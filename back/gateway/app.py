"""
Gateway service. This is an entrypoint to the API
"""

from http import HTTPStatus
from rb_queue import Queue

import requests
import variables
import utils

from flask import Flask, request, make_response
from flask_cors import CORS
from authentication import requires_authentication
from mongodb import MongoDB, RedundantException


app = Flask(__name__)
CORS(app)

mongo = MongoDB(app, variables.MONGODB)

rb_queue = Queue(
    variables.RABBITMQ_HOST,
    variables.RABBITMQ_SVC_USER,
    variables.RABBITMQ_SVC_PASSWORD,
)


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
        variables.AUTH_SERVICE_LOGIN, auth=basic_auth, timeout=10
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

    try:
        video_id = utils.extract_video_id(youtube_url)
    except RuntimeError as error:
        return f"Wrong YouTube Video URL: {error}", HTTPStatus.BAD_REQUEST

    try:
        mongo.insert_user(email, video_id)
        mongo.insert_job(youtube_url, video_id)
    except RedundantException:
        return "You already have downloaded this", HTTPStatus.BAD_REQUEST

    rb_queue.publish_job(youtube_url, video_id)

    return "OK"


@app.route("/items", methods=["GET"])
@requires_authentication
def get_items(user: dict):
    """Returns a list of items for an authenticated user"""
    return mongo.get_user_items(user["email"])


@app.route("/terminate/<video_id>", methods=["DELETE"])
@requires_authentication
def terminate(user: dict, video_id: str):
    """Removes item from the user"""
    mongo.remove_item_from_user(user["email"], video_id)
    return "OK", HTTPStatus.OK


@app.route("/retry/<video_id>", methods=["POST"])
@requires_authentication
def retry(user: dict, video_id: str):
    """Retries downloading process of given video id"""
    if mongo.has_user_video(user["email"], video_id):
        url = mongo.get_youtube_url(video_id)
        rb_queue.publish_job(url, video_id)
        mongo.set_queued_state(video_id)
        return "OK", HTTPStatus.OK
    return (
        f"User does not own the item with ID {video_id}",
        HTTPStatus.BAD_REQUEST,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
