import factory
from faker import Faker
from app import db
from app.models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
    
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyAttribute(
        lambda x: fake.credit_card_number() if fake.boolean() else None
    )
    car_number = factory.Faker('text', max_nb_chars=10)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
    
    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=10, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
