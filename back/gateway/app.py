"""
Gateway service
"""

import json
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import os, requests

app = Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint to perform authentication
    """
    auth = request.authorization
    if not auth:
        return "Requires Basic Auth", 401
    basic_auth = (auth.username, auth.password)
    resp = requests.post("http://localhost:5000/login", auth=basic_auth)

    if resp.status_code == 200:
        response = make_response("OK")
        response.set_cookie("JWT", resp.text, max_age=14400)
        return response
    elif resp.status_code == 401:
        return "Invalid credentials", 401
    return f"Internal service failed: <{resp.status_code}> {resp.text}"


@app.route("/validate-token", methods=["GET"])
def validate_jwt():
    jwt = request.cookies.get("JWT")

    if not jwt:
        return "Missing JWT", 401

    resp = requests.post(
        "http://localhost:5000/validate", headers={"Authorization": f"Bearer {jwt}"}
    )

    if resp.status_code != 200:
        return "Token broken", 401

    return "Token OK", 200


@app.after_request
def apply_headings(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/test")
def test():
    print(request.cookies)
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
