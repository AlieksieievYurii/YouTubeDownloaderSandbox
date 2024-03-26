"""Unittests for utils"""

from src import utils


def test_create_jwt():
    """Validates jwt util functions"""
    key = "1234"
    email = "test@email.com"
    encoded = utils.create_jwt("test@email.com", key)
    decoded = utils.decode_jwt(encoded, key)

    assert decoded["email"] == email
