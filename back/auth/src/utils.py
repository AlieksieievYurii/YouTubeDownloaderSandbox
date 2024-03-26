"""Utils file"""

import datetime
from typing import Dict, Optional
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


def decode_jwt(encoded_jwt: str, secret: str) -> Optional[Dict]:
    """Decodes given JWT"""
    try:
        return jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
