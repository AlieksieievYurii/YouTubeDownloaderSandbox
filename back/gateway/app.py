"""
Gateway service. This is an entrypoint to the API
"""

import requests

from flask import Flask, request, make_response
from flask_cors import CORS
from authentication import requires_authentication
import variables
from http import HTTPStatus

app = Flask(__name__)
CORS(app)


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
def validate_jwt():
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


@app.route("/test")
@requires_authentication
def test():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
