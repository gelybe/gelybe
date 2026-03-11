from flask import Flask, request, jsonify
from models import db, Room, Booking
from logic import add_room, get_available_rooms, book_room, get_room_by_id
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/v1/rooms', methods=['POST'])
def add_room_endpoint():
    data = request.get_json()
    floor = data['floor']
    beds = data['beds']
    guest_count = data['guest_count']
    price = data['price']
    room = add_room(floor, beds, guest_count, price)
    return jsonify({
        'room': room.to_dict(),
        'links': {
            'self': f'/api/v1/rooms/{room.id}',
            'collection': '/api/v1/rooms'
        }
    }), 201

@app.route('/api/v1/rooms', methods=['GET'])
def get_rooms_endpoint():
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    guest_count_str = request.args.get('guest_count')
    guest_count = int(guest_count_str) if guest_count_str is not None else None
    rooms = get_available_rooms(check_in, check_out, guest_count)
    return jsonify({
        'rooms': rooms,
        'links': {
            'self': '/api/v1/rooms'
        }
    })

@app.route('/api/v1/rooms/<int:room_id>', methods=['GET'])
def get_room_endpoint(room_id):
    room = get_room_by_id(room_id)
    return jsonify({
        'room': room,
        'links': {
            'self': f'/api/v1/rooms/{room_id}',
            'collection': '/api/v1/rooms'
        }
    })

@app.route('/api/v1/bookings', methods=['POST'])
def booking_endpoint():
    data = request.get_json()
    booking_dates = data['booking_dates']
    check_in = str(booking_dates['check_in'])
    check_out = str(booking_dates['check_out'])
    first_name = data['first_name']
    last_name = data['last_name']
    room_id = data['room_id']
    try:
        booking = book_room(room_id, check_in, check_out, first_name, last_name)
        return jsonify({
            'booking': {
                'id': booking.id,
                'room_id': booking.room_id,
                'check_in': booking.check_in,
                'check_out': booking.check_out,
                'first_name': booking.first_name,
                'last_name': booking.last_name
            },
            'links': {
                'self': f'/api/v1/bookings/{booking.id}',
                'collection': '/api/v1/bookings'
            }
        }), 201
    except ValueError:
        return jsonify({'error': 'Room already booked'}), 409

if __name__ == '__main__':
    app.run(debug=True)
