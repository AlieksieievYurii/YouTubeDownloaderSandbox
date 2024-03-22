"""
Gateway service. This is an entrypoint to the API
"""

from http import HTTPStatus
import json

import requests
import variables
import utils
import pika

from flask import Flask, request, make_response
from flask_cors import CORS
from authentication import requires_authentication
from mongodb import MongoDB, RedundantException


app = Flask(__name__)
CORS(app)

mongo = MongoDB(app, variables.MONGODB)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        variables.RABBITMQ_HOST,
        credentials=pika.PlainCredentials(
            username=variables.RABBITMQ_SVC_USER,
            password=variables.RABBITMQ_SVC_PASSWORD,
        ),
    )
)
channel = connection.channel()


@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint to perform authentication.
    The client must use Basic Auth
    """
    auth = request.authorization
    if not auth:
        return "Requires Basic Auth", 401
    basic_auth = (auth.username, auth.password)
    resp = requests.post(
        variables.AUTH_SERVICE_LOGIN, auth=basic_auth, timeout=None
    )

    if resp.status_code == 200:
        response = make_response("OK")
        response.set_cookie("JWT", resp.text, max_age=14400)
        return response
    if resp.status_code == 401:
        return "Invalid credentials", 401
    return f"Internal service failed: <{resp.status_code}> {resp.text}"


@app.route("/validate-token", methods=["GET"])
@requires_authentication
def validate_jwt(_: dict):
    """
    Validates the given token.
    The token is taken from the cookies
    """
    return HTTPStatus.OK.phrase


@app.after_request
def apply_headings(response):
    """
    Adds neccessary headers to each request
    """
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/queue", methods=["POST"])
@requires_authentication
def queue(user: dict):
    """Puts the given youtube url into queue for downloading"""
    email = user["email"]
    youtube_url = request.json.get("youtube_url")

    if not youtube_url:
        return "youtube_url must be defined in body!", HTTPStatus.BAD_REQUEST

    video_id = utils.extract_video_id(youtube_url)

    try:
        mongo.insert_user(email, video_id)
        mongo.insert_job(youtube_url, video_id)
    except RedundantException:
        return "You already have this video", HTTPStatus.BAD_REQUEST

    channel.basic_publish(
        exchange="",
        routing_key="jobs",
        body=json.dumps({"url": youtube_url, "video_id": video_id}),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )

    return "OK"


if __name__ == "__main__":
    channel.queue_declare(queue="jobs")
    app.run(host="0.0.0.0", port=8080)
