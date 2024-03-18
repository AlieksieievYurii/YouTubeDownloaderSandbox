"""Util file that provides operational variables"""

import os
from typing import Optional


def _load_env_variable(name: str, default: Optional[str] = None) -> str:
    value = os.environ.get(name)
    if value:
        return value

    if not value and default:
        return default

    raise RuntimeError(f"Environment variable '{name}' is not defined")


AUTH_SERVICE_HOST = _load_env_variable("AUTH_SERVICE_HOST", "localhost")
AUTH_SERVICE_PORT = _load_env_variable("AUTH_SERVICE_HOST", "5000")
AUTH_SERVICE_URL = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}"
AUTH_SERVICE_LOGIN = f"{AUTH_SERVICE_URL}/login"
AUTH_SERVICE_VALIDATE = f"{AUTH_SERVICE_URL}/validate"
