import requests

from http import HTTPStatus
from flask import Blueprint, current_app, request
from flask import request, make_response, send_file

from . import utils
from . import variables
from .authentication import requires_authentication
from .mongodb import RedundantException


gateway = Blueprint("gateway", __name__)


@gateway.route("/login", methods=["POST"])
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

    return (
        f"Internal service failed: <{resp.status_code}> {resp.text}",
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@gateway.route("/validate-token", methods=["GET"])
@requires_authentication
def validate_jwt(_: dict):
    """
    Validates the given token.
    The token is taken from the cookies
    """
    return HTTPStatus.OK.phrase


@gateway.after_request
def apply_headings(response):
    """
    Adds neccessary headers to each request
    """
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@gateway.route("/queue", methods=["POST"])
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
        current_app.mongo.insert_user(email, video_id)
        if not current_app.mongo.item_exists(video_id):
            current_app.mongo.insert_job(youtube_url, video_id)
            current_app.rb_queue.publish_job(youtube_url, video_id)
    except RedundantException:
        return "You already have downloaded this", HTTPStatus.BAD_REQUEST

    return "OK"


@gateway.route("/items", methods=["GET"])
@requires_authentication
def get_items(user: dict):
    """Returns a list of items for an authenticated user"""
    return current_app.mongo.get_user_items(user["email"])


@gateway.route("/terminate/<video_id>", methods=["DELETE"])
@requires_authentication
def terminate(user: dict, video_id: str):
    """Removes item from the user"""
    current_app.mongo.remove_item_from_user(user["email"], video_id)
    return "OK", HTTPStatus.OK


@gateway.route("/retry/<video_id>", methods=["POST"])
@requires_authentication
def retry(user: dict, video_id: str):
    """Retries downloading process of given video id"""
    if current_app.mongo.has_user_video(user["email"], video_id):
        url = current_app.mongo.get_youtube_url(video_id)
        current_app.rb_queue.publish_job(url, video_id)
        current_app.mongo.set_queued_state(video_id)
        return "OK", HTTPStatus.OK
    return (
        f"User does not own the item with ID {video_id}",
        HTTPStatus.BAD_REQUEST,
    )


@gateway.route("/download/<video_id>", methods=["GET"])
@requires_authentication
def download(user: dict, video_id: str):
    """Sends audio file to the caller"""
    if current_app.mongo.has_user_video(user["email"], video_id):
        return send_file(
            current_app.mongo.get_audio_file(video_id),
            download_name=f"{video_id}.mp3",
            as_attachment=True,
        )
    return (
        f"User does not own the item with ID {video_id}",
        HTTPStatus.BAD_REQUEST,
    )
