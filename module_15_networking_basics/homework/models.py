from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, nullable=False)
    beds = db.Column(db.Integer, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'room_id': self.id,
            'floor': self.floor,
            'beds': self.beds,
            'guest_count': self.guest_count,
            'price': self.price
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.String(8), nullable=False)  # YYYYMMDD
    check_out = db.Column(db.String(8), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
