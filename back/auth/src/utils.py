"""Utils file"""

import datetime
import jwt


def create_jwt(email: str, secret: str) -> str:
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
        secret,
        algorithm="HS256",
    )
