"""Provides stuff for handling authentication"""

import functools
from http import HTTPStatus
import requests
import variables

from flask import request


def is_jwt_valid(jwt: str) -> bool:
    """Validates the given JWT token. Using Auth service for that"""
    respoce = requests.post(
        variables.AUTH_SERVICE_VALIDATE,
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=None,
    )
    if respoce.status_code != HTTPStatus.OK:
        print(f"Token validation failed. Error<{respoce.status_code}>: {respoce.text}")
    return respoce.status_code == HTTPStatus.OK


def requires_authentication(fun):
    """Decorator that checks user authentication"""

    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        jwt = request.cookies.get("JWT")
        if not jwt:
            return "Missing cookie with JWT", HTTPStatus.UNAUTHORIZED

        if is_jwt_valid(jwt):
            return fun(*args, **kwargs)

        return "JWT token is invalid", HTTPStatus.UNAUTHORIZED

    return wrapper
