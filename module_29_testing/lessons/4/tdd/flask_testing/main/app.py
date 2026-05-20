from flask import Flask
from .config import config_by_name


def create_app(config_var: str) -> Flask:
    app = Flask(__name__)
    config = config_by_name[config_var]
    app.config.from_object(config)

    return app
