import pytest
from app import db
from app.models import Client, Parking
from factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(client, database):
    # Создаем клиента через фабрику
    new_client = ClientFactory()
    db.session.commit()
    
    # Проверяем, что клиент создан
    assert new_client.id is not None
    assert new_client.name is not None
    assert new_client.surname is not None
    
    # Проверяем, что количество клиентов увеличилось
    client_count = Client.query.count()
    assert client_count == 2


def test_create_parking_with_factory(client, database):
    # Создаем парковку через фабрику
    new_parking = ParkingFactory()
    db.session.commit()
    
    # Проверяем, что парковка создана
    assert new_parking.id is not None
    assert new_parking.address is not None
    assert new_parking.count_places is not None
    assert new_parking.count_available_places == new_parking.count_places
    
    # Проверяем, что количество парковок увеличилось
    parking_count = Parking.query.count()
    assert parking_count == 2
