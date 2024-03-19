"""
Gateway service. This is an entrypoint to the API
"""

import requests

from flask_pymongo import PyMongo
from flask import Flask, request, make_response
from flask_cors import CORS
from authentication import requires_authentication
import variables
from http import HTTPStatus

app = Flask(__name__)
CORS(app)

mongo = PyMongo(app, uri=variables.MONGODB)
mongo_users = mongo.cx.get_database("users_db")["users"]


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
    resp = requests.post(variables.AUTH_SERVICE_LOGIN, auth=basic_auth, timeout=None)

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
    body = request.json.get("youtube_url")
    if not body:
        return "youtube_url must be defined in body!", HTTPStatus.BAD_REQUEST

    if not list(mongo_users.find({"email": email})):
        mongo_users.insert_one({"email": email})

    if list(mongo_users.find({"email": email, "videos": body})):
        return "You already have this video", HTTPStatus.BAD_REQUEST

    mongo_users.update_one({"email": email}, {"$push": {"videos": body}})

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
