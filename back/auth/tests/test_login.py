from base64 import b64encode
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    ("email", "password", "status"),
    (
        ("yurii", "1234", 200),
        ("yurii", "12", 401),
        ("lol", "test", 401),
    ),
)
def test__login(client, email, password, status):
    credentials = b64encode(f"{email}:{password}".encode())
    resp = client.post(
        "/login", headers={"Authorization": f"Basic {credentials.decode()}"}
    )

    assert resp.status_code == status


@patch("src.views.utils.decode_jwt")
def test_validate(decode_jwt, client):
    decode_jwt.return_value = {"email": "test"}
    resp = client.post("/validate", headers={"Authorization": "Bearer token"})

    assert resp.status_code == 200
