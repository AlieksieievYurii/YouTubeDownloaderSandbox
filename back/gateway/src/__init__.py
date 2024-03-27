from flask import Flask
from flask_cors import CORS

from . import variables

from .mongodb import MongoDB
from .rb_queue import Queue
from .views import gateway


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    CORS(app)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.mongo = MongoDB(app, variables.MONGODB)
        app.rb_queue = Queue(
            variables.RABBITMQ_HOST,
            variables.RABBITMQ_SVC_USER,
            variables.RABBITMQ_SVC_PASSWORD,
        )

    app.register_blueprint(gateway)

    return app
