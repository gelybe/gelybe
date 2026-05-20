import pytest
from flask import template_rendered
from flask_testing.main.app import create_app, db as _db
from flask_testing.main.models import Product, User


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        user = User(id=1,
                    name="name",
                    surname="surname",
                    email='mail')
        product = Product(title="title",
                          price=500,
                          user_id=1)
        _db.session.add(user)
        _db.session.add(product)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
