"""Provides stuff for handling authentication"""

import functools
from http import HTTPStatus
from typing import Tuple
import requests
import variables

from flask import request


def validate_jwt(jwt: str) -> Tuple[bool, str]:
    """Validates the given JWT token. Using Auth service for that"""
    response = requests.post(
        variables.AUTH_SERVICE_VALIDATE,
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=None,
    )
    if response.status_code != HTTPStatus.OK:
        print(
            f"Token validation failed. Error<{response.status_code}>: {response.text}"
        )

    return response.status_code == HTTPStatus.OK, response.json()


def requires_authentication(fun):
    """Decorator that checks user authentication"""

    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        jwt = request.cookies.get("JWT")
        if not jwt:
            return "Missing cookie with JWT", HTTPStatus.UNAUTHORIZED
        is_valid, data = validate_jwt(jwt)
        if is_valid:
            return fun(data, *args, **kwargs)

        return "JWT token is invalid", HTTPStatus.UNAUTHORIZED

    return wrapper
