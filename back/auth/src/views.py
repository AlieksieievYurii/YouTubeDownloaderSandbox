"""Contains different endpoint(views)"""

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

    res = current_app.auth_db.get_user(request.authorization.username)

    if not res or (
        request.authorization.username != res[0]
        or request.authorization.password != res[1]
    ):
        return "invalid creadentials", 401

    return utils.create_jwt(
        request.authorization.username, current_app.config["JWT_SECRET"]
    )


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
