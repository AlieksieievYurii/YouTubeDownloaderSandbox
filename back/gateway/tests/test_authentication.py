from base64 import b64encode
from unittest.mock import Mock, patch


@patch("src.views.requests")
def test_successful_login(requests, client):
    email = "test@gmail.com"
    password = "1234"

    a = Mock(name="Responce", status_code=200, text="jwt1234")
    requests.post.return_value = a

    credentials = b64encode(f"{email}:{password}".encode())
    resp = client.post(
        "/login", headers={"Authorization": f"Basic {credentials.decode()}"}
    )

    assert resp.status_code == 200
    for k, v in resp.headers:
        if k == "Set-Cookie":
            assert v.split(";")[0] == "JWT=jwt1234"
            break
    else:
        assert False, "Set-Cookie header is not found in login response"


@patch("src.views.requests")
def test_bad_login(requests, client):
    email = "test@gmail.com"
    password = "1234"

    a = Mock(name="Responce", status_code=401)
    requests.post.return_value = a

    credentials = b64encode(f"{email}:{password}".encode())
    resp = client.post(
        "/login", headers={"Authorization": f"Basic {credentials.decode()}"}
    )

    assert resp.status_code == 401


@patch("src.authentication.validate_jwt", return_value=(True, "some data"))
def test_validate_token(validate_jwt, client):
    client.set_cookie("JWT", "exp")
    resp = client.get("/validate-token")

    assert resp.status_code == 200
    validate_jwt.assert_called_once()
