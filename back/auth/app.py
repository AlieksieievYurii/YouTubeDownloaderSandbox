"""
This is authentication service
"""

import os
import datetime
import sys

from flask import Flask, request
from flask_mysqldb import MySQL
import jwt

server = Flask(__name__)
mysql = MySQL(server)


def require_env(key: str) -> str:
    """Ensures that given env variable exists"""
    value = os.environ.get(key)
    if not value:
        print(f"Env var '{key}' must be defined!")
        sys.exit(1)
    return value


server.config["JWT_SECRET"] = require_env("JWT_SECRET")

server.config["MYSQL_HOST"] = require_env("MYSQL_HOST")
server.config["MYSQL_USER"] = require_env("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = require_env("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = require_env("MYSQL_DB")
server.config["MYSQL_PORT"] = int(require_env("MYSQL_PORT"))


@server.route("/login", methods=["POST"])
def login():
    """
    Performs login process
    """

    if not request.authorization:
        return "missing credentials", 401

    cur = mysql.connection.cursor()

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

        return create_jwt(request.authorization.username)

    return "invalid credentials", 401


def create_jwt(email: str):
    """Creates JWT"""
    expiration_date = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=1)

    return jwt.encode(
        {
            "email": email,
            "exp": expiration_date,
            "iat": datetime.datetime.now(datetime.UTC),
        },
        server.config["JWT_SECRET"],
        algorithm="HS256",
    )


@server.route("/validate", methods=["POST"])
def validate():
    """Validates JWT"""
    encoded_jwt = request.headers["Authorization"]
    print(encoded_jwt)
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split()[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, server.config["JWT_SECRET"], algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        return "not athorized", 401

    return decoded, 200


if __name__ == "__main__":
    # This is essential to set host to 0.0.0.0
    # if we want to make the server listen to external incoming requests
    server.run(host="0.0.0.0", port=5000)
