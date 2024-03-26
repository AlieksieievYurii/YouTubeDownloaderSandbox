"""Contains different endpoint(views)"""

import jwt

from flask import Blueprint, current_app, request

from . import utils

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    Performs login process
    """

    if not request.authorization:
        return "missing credentials", 401

    cur = current_app.auth_db.connection.cursor()

    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s",
        (request.authorization.username,),
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if (
            request.authorization.username != email
            or request.authorization.password != password
        ):
            return "invalid creadentials", 401

        return utils.create_jwt(
            request.authorization.username, current_app.config["JWT_SECRET"]
        )

    return "invalid credentials", 401


@auth_blueprint.route("/validate", methods=["POST"])
def validate():
    """Validates JWT"""
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split()[1]

    decoded = utils.decode_jwt(encoded_jwt, current_app.config["JWT_SECRET"])
    if not decoded:
        return "not athorized", 401

    return decoded, 200
