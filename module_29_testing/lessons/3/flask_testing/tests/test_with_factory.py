from .factories import UserFactory, ProductFactory
from flask_testing.main.models import Product, User


def test_create_user(app, db):
    user = UserFactory()
    db.session.commit()
    assert user.id is not None
    assert len(db.session.query(User).all()) == 2


def test_create_product(client, db):
    product = ProductFactory()
    db.session.commit()
    assert product.id is not None
    assert product.user.id is not None
    assert len(db.session.query(Product).all()) == 2
