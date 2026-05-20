from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import Client, Parking, ClientParking

bp = Blueprint('api', __name__)


@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients]), 200


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict()), 200


@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201


@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.get_json()
    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify(parking.to_dict()), 201


@bp.route('/client_parkings', methods=['POST'])
def client_parking_enter():
    data = request.get_json()
    client_id = data['client_id']
    parking_id = data['parking_id']
    
    parking = Parking.query.get_or_404(parking_id)
    
    if not parking.opened:
        return jsonify({'error': 'Parking is closed'}), 400
    
    if parking.count_available_places <= 0:
        return jsonify({'error': 'No available places'}), 400
    
    existing = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first()
    
    if existing:
        return jsonify({'error': 'Client already on this parking'}), 400
    
    client_parking = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.utcnow()
    )
    
    parking.count_available_places -= 1
    
    db.session.add(client_parking)
    db.session.commit()
    
    return jsonify(client_parking.to_dict()), 201


@bp.route('/client_parkings', methods=['DELETE'])
def client_parking_exit():
    data = request.get_json()
    client_id = data['client_id']
    parking_id = data['parking_id']
    
    client = Client.query.get_or_404(client_id)
    
    if not client.credit_card:
        return jsonify({'error': 'Client has no credit card'}), 400
    
    client_parking = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first_or_404()
    
    if client_parking.time_out:
        return jsonify({'error': 'Client already left'}), 400
    
    parking = Parking.query.get_or_404(parking_id)
    
    client_parking.time_out = datetime.utcnow()
    
    if client_parking.time_out < client_parking.time_in:
        return jsonify({'error': 'Time out cannot be less than time in'}), 400
    
    parking.count_available_places += 1
    
    db.session.commit()
    
    return jsonify(client_parking.to_dict()), 200
