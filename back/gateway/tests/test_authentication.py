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


