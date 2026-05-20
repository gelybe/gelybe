import json
import pytest


def test_math_route(client) -> None:
    resp = client.get("/test_route?number=8")
    data = json.loads(resp.data.decode())
    assert data == 64


def test_user(client) -> None:
    resp = client.get("/users/1")
    assert resp.status_code == 200
    assert resp.json == {"id": 1, "name": "name", "surname": "surname",
                         "email": "mail"}


def test_create_user(client) -> None:
    user_data = {"name": "Никита", "surname": "Нестеренко",
                 "email": "mail"}
    resp = client.post("/users", data=user_data)

    assert resp.status_code == 201


def test_app_config(app):
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite://"


def test_render_jinja2(client, captured_templates) -> None:
    route = "/"
    resp = client.get(route)
    assert resp.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "user_products.html"
    assert context["products"]
    products = context["products"]
    assert products[0]["title"] == "title"


@pytest.mark.parametrize("route", ["/test_route?number=8", "/users/1",
                                   "/users", "/"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200
