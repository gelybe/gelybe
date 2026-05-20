import pytest
from app import db
from app.models import Client, Parking, ClientParking


@pytest.mark.parametrize('endpoint', [
    '/clients',
    '/clients/1'
])
def test_get_methods_return_200(client, database, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


def test_create_client(client, database):
    data = {
        'name': 'Ivan',
        'surname': 'Ivanov',
        'credit_card': '9876543210987654',
        'car_number': 'B456CD'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    
    response_data = response.get_json()
    assert response_data['name'] == 'Ivan'
    assert response_data['surname'] == 'Ivanov'
    assert response_data['credit_card'] == '9876543210987654'
    assert response_data['car_number'] == 'B456CD'
    assert 'id' in response_data
    
    client_count = Client.query.count()
    assert client_count == 2


def test_create_parking(client, database):
    data = {
        'address': 'New Street 10',
        'opened': True,
        'count_places': 20
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    
    response_data = response.get_json()
    assert response_data['address'] == 'New Street 10'
    assert response_data['opened'] == True
    assert response_data['count_places'] == 20
    assert response_data['count_available_places'] == 20
    assert 'id' in response_data
    
    parking_count = Parking.query.count()
    assert parking_count == 2


@pytest.mark.parking
def test_client_parking_enter(client, database):
    # Создаем нового клиента с картой
    new_client = Client(
        name='Petr',
        surname='Petrov',
        credit_card='1111222233334444',
        car_number='C789DE'
    )
    db.session.add(new_client)
    
    # Создаем новую парковку
    new_parking = Parking(
        address='Enter Test Street',
        opened=True,
        count_places=5,
        count_available_places=5
    )
    db.session.add(new_parking)
    db.session.commit()
    
    data = {
        'client_id': new_client.id,
        'parking_id': new_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 201
    
    response_data = response.get_json()
    assert response_data['client_id'] == new_client.id
    assert response_data['parking_id'] == new_parking.id
    assert response_data['time_in'] is not None
    assert response_data['time_out'] is None
    
    # Проверяем, что количество свободных мест уменьшилось
    parking = Parking.query.get(new_parking.id)
    assert parking.count_available_places == 4
    
    # Проверяем, что парковка открыта
    assert parking.opened == True


@pytest.mark.parking
def test_client_parking_exit(client, database):
    # Создаем нового клиента с картой
    new_client = Client(
        name='Sidor',
        surname='Sidorov',
        credit_card='5555666677778888',
        car_number='F012GH'
    )
    db.session.add(new_client)
    
    # Создаем новую парковку
    new_parking = Parking(
        address='Exit Test Street',
        opened=True,
        count_places=5,
        count_available_places=5
    )
    db.session.add(new_parking)
    db.session.commit()
    
    # Заезжаем на парковку
    enter_data = {
        'client_id': new_client.id,
        'parking_id': new_parking.id
    }
    client.post('/client_parkings', json=enter_data)
    
    # Выезжаем с парковки
    exit_data = {
        'client_id': new_client.id,
        'parking_id': new_parking.id
    }
    response = client.delete('/client_parkings', json=exit_data)
    assert response.status_code == 200
    
    response_data = response.get_json()
    assert response_data['client_id'] == new_client.id
    assert response_data['parking_id'] == new_parking.id
    assert response_data['time_in'] is not None
    assert response_data['time_out'] is not None
    
    # Проверяем, что количество свободных мест увеличилось
    parking = Parking.query.get(new_parking.id)
    assert parking.count_available_places == 5
    
    # Проверяем, что время выезда больше времени заезда
    client_parking = ClientParking.query.filter_by(
        client_id=new_client.id,
        parking_id=new_parking.id
    ).first()
    assert client_parking.time_out > client_parking.time_in


def test_parking_enter_closed(client, database):
    # Создаем закрытую парковку
    closed_parking = Parking(
        address='Closed Street',
        opened=False,
        count_places=10,
        count_available_places=10
    )
    db.session.add(closed_parking)
    
    new_client = Client(
        name='Test',
        surname='User',
        credit_card='9999888877776666',
        car_number='I345JK'
    )
    db.session.add(new_client)
    db.session.commit()
    
    data = {
        'client_id': new_client.id,
        'parking_id': closed_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Parking is closed'


def test_parking_enter_no_places(client, database):
    # Создаем парковку без свободных мест
    full_parking = Parking(
        address='Full Street',
        opened=True,
        count_places=0,
        count_available_places=0
    )
    db.session.add(full_parking)
    
    new_client = Client(
        name='Test',
        surname='User',
        credit_card='9999888877776666',
        car_number='L678MN'
    )
    db.session.add(new_client)
    db.session.commit()
    
    data = {
        'client_id': new_client.id,
        'parking_id': full_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No available places'


def test_parking_exit_no_card(client, database):
    # Создаем клиента без карты
    client_no_card = Client(
        name='NoCard',
        surname='User',
        car_number='O901PQ'
    )
    db.session.add(client_no_card)
    
    new_parking = Parking(
        address='No Card Street',
        opened=True,
        count_places=5,
        count_available_places=5
    )
    db.session.add(new_parking)
    db.session.commit()
    
    # Заезжаем на парковку
    enter_data = {
        'client_id': client_no_card.id,
        'parking_id': new_parking.id
    }
    client.post('/client_parkings', json=enter_data)
    
    # Пытаемся выехать
    exit_data = {
        'client_id': client_no_card.id,
        'parking_id': new_parking.id
    }
    response = client.delete('/client_parkings', json=exit_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Client has no credit card'
