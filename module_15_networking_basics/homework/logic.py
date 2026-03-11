from models import db, Room, Booking
from datetime import datetime

def add_room(floor, beds, guest_num, price):
    room = Room(floor=floor, beds=beds, guest_num=guest_num, price=price)
    db.session.add(room)
    db.session.commit()

def get_available_rooms(check_in, check_out, guests_num):
    if guests_num is None:
        guests_num = 1
    # Get all rooms that can accommodate the number of guests
    rooms = Room.query.filter(Room.guest_num >= guests_num).all()
    available_rooms = []
    for room in rooms:
        if check_in is None or check_out is None:
            # No date filter, room is available
            available_rooms.append(room.to_dict())
        else:
            # Check if room is booked in the date range
            overlapping_bookings = Booking.query.filter(
                Booking.room_id == room.id,
                Booking.check_in < check_out,
                Booking.check_out > check_in
            ).first()
            if not overlapping_bookings:
                available_rooms.append(room.to_dict())
    return available_rooms

def book_room(room_id, check_in, check_out, first_name, last_name):
    # Check if room is available
    overlapping = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).first()
    if overlapping:
        raise ValueError("Room already booked")
    
    booking = Booking(room_id=room_id, check_in=check_in, check_out=check_out, 
                     first_name=first_name, last_name=last_name)
    db.session.add(booking)
    db.session.commit()
