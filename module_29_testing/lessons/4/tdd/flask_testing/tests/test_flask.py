from flask_testing.main.app import create_app
from flask import Flask


def test_create_app():
    app = create_app()
    assert isinstance(app, Flask)
