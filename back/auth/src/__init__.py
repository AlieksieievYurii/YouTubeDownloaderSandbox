"""
This is authentication service
"""

import os
import sys
from flask import Flask
from flask_mysqldb import MySQL

from .db import AuthDB
from . import views


def require_env(key: str) -> str:
    """Ensures that given env variable exists"""
    value = os.environ.get(key)
    if not value:
        print(f"Env var '{key}' must be defined!")
        sys.exit(1)
    return value


def create_app(test_config=None) -> Flask:
    """Factory function to create Flask application"""
    app = Flask(__name__)

    if test_config:
        app.auth_db = test_config.pop("AUTH_DB")
        app.config.from_mapping(test_config)
    else:
        app.config["JWT_SECRET"] = require_env("JWT_SECRET")
        app.config["MYSQL_HOST"] = require_env("MYSQL_HOST")
        app.config["MYSQL_USER"] = require_env("MYSQL_USER")
        app.config["MYSQL_PASSWORD"] = require_env("MYSQL_PASSWORD")
        app.config["MYSQL_DB"] = require_env("MYSQL_DB")
        app.config["MYSQL_PORT"] = int(require_env("MYSQL_PORT"))

        app.auth_db = AuthDB(app)

    app.register_blueprint(views.auth_blueprint)

    return app
