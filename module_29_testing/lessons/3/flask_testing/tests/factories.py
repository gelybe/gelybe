import factory
import factory.fuzzy as fuzzy
import random

from flask_testing.main.app import db
from flask_testing.main.models import User, Product


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.name)


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session

    title = fuzzy.FuzzyText(prefix='Продукт ')
    price = factory.LazyAttribute(lambda x: random.randrange(0, 10000))
    user = factory.SubFactory(UserFactory)
