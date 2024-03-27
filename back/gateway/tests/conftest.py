import sys
import pathlib

from flask import Flask
import pytest

auth_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.append(str(auth_dir))

# pylint: disable=C0413:wrong-import-position
from src import create_app


@pytest.fixture
def app():

    flask_app = create_app({"TESTING": True, "JWT_SECRET": "1234"})

    yield flask_app


@pytest.fixture
# pylint: disable=W0621:redefined-outer-name
def client(app: Flask):
    return app.test_client()
