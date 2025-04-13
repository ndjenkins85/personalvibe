# Copyright © 2025 by Nick Jenkins. All rights reserved

from flask import Flask
from flask_cors import CORS
from flask_sslify import SSLify


def create_app() -> Flask:
    """Creates the primary Flask app with config.

    Returns:
        Flask: returns flask app.
    """
    app = Flask(__name__)
    # app.config.from_object("personalvibe.config.config.Config")
    return app


app = create_app()
CORS(app)
sslify = SSLify(app)

# import personalvibe.views  # noqa: E402
