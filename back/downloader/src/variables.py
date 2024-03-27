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


RABBITMQ_HOST = _load_env_variable("RABBITQM_HOST", "localhost")
RABBITMQ_SVC_USER = _load_env_variable("RABBITMQ_SVC_USER", "yurii")
RABBITMQ_SVC_PASSWORD = _load_env_variable("RABBITMQ_SVC_PASSWORD", "yurii")

MONGODB_HOST = _load_env_variable("MONGODB_HOST", "localhost")
MONGODB_PORT = _load_env_variable("MONGODB_PORT", "27017")
MONGODB_USERNAME = _load_env_variable("MONGODB_USERNAME", "yurii")
MONGODB_PASSWORD = _load_env_variable("MONGODB_PASSWORD", "yurii")

MONGODB = (
    f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}"
    + f"@{MONGODB_HOST}:{MONGODB_PORT}"
)
