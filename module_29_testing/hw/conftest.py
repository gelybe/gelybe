import pytest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Client, Parking, ClientParking
from factories import ClientFactory, ParkingFactory


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        
        # Настраиваем сессию для фабрик
        ClientFactory._meta.sqlalchemy_session = db.session
        ParkingFactory._meta.sqlalchemy_session = db.session
        
        # Создаем тестового клиента
        test_client = Client(
            name='Test',
            surname='User',
            credit_card='1234567890123456',
            car_number='A123BC'
        )
        db.session.add(test_client)
        
        # Создаем тестовую парковку
        test_parking = Parking(
            address='Test Street 1',
            opened=True,
            count_places=10,
            count_available_places=10
        )
        db.session.add(test_parking)
        
        # Создаем тестовый лог въезда-выезда
        time_in = datetime.utcnow() - timedelta(hours=2)
        time_out = datetime.utcnow() - timedelta(hours=1)
        test_client_parking = ClientParking(
            client_id=test_client.id,
            parking_id=test_parking.id,
            time_in=time_in,
            time_out=time_out
        )
        db.session.add(test_client_parking)
        
        db.session.commit()
        
        yield db
        
        db.session.remove()
        db.drop_all()
