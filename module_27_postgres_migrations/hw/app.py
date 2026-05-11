import os
import random
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy import func, text
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql+psycopg://skillbox_user:skillbox_pass@localhost:5432/skillbox_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Coffee(db.Model):
    __tablename__ = 'coffee'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))
    reviews = db.Column(ARRAY(db.String))

    users = db.relationship('User', backref='coffee', lazy=True)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    has_sale = db.Column(db.Boolean, default=False)
    address = db.Column(JSON)
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'), nullable=True)


@app.before_request
def create_tables_once():
    with app.app_context():
        db.create_all()
        init_data()
    app.before_request_funcs[None].remove(create_tables_once)


def init_data():
    """Инициализация тестовых данных."""
    if Coffee.query.first() or User.query.first():
        return

    # Получаем данные о кофе из DummyJSON
    coffee_response = requests.get('https://dummyjson.com/products/search?q=coffee')
    coffee_data = coffee_response.json()

    coffee_obj = None
    if coffee_data.get('products'):
        product = coffee_data['products'][0]
        reviews_list = []
        if product.get('reviews'):
            reviews_list = [r.get('comment', '') for r in product['reviews']]

        coffee_obj = Coffee(
            title=product.get('title', ''),
            category=product.get('category', ''),
            description=product.get('description', ''),
            reviews=reviews_list
        )
        db.session.add(coffee_obj)
        db.session.commit()

    # Получаем пользователей из DummyJSON
    users_response = requests.get('https://dummyjson.com/users?limit=10')
    users_data = users_response.json()

    for user_data in users_response.json().get('users', []):
        address = {
            'country': user_data.get('address', {}).get('country', ''),
            'city': user_data.get('address', {}).get('city', ''),
            'address': user_data.get('address', {}).get('address', '')
        }
        coffee_id = coffee_obj.id if coffee_obj else None

        user = User(
            name=user_data.get('firstName', ''),
            has_sale=random.choice([True, False]),
            address=address,
            coffee_id=coffee_id
        )
        db.session.add(user)

    db.session.commit()


@app.route('/users', methods=['POST'])
def add_user():
    """Добавление пользователя с предпочтением по кофе."""
    data = request.get_json() or {}

    coffee_id = data.get('coffee_id')
    coffee = Coffee.query.get(coffee_id) if coffee_id else None

    user = User(
        name=data.get('name', ''),
        has_sale=data.get('has_sale', False),
        address=data.get('address', {}),
        coffee_id=coffee_id
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'name': user.name,
        'has_sale': user.has_sale,
        'address': user.address,
        'coffee': {
            'id': coffee.id,
            'title': coffee.title
        } if coffee else None
    })


@app.route('/coffee/search')
def search_coffee():
    """Полнотекстовый поиск кофе по названию."""
    title = request.args.get('title', '')

    # Полнотекстовый поиск с использованием to_tsvector
    results = db.session.query(Coffee).filter(
        text("to_tsvector('english', title) @@ plainto_tsquery('english', :query)").bindparams(query=title)
    ).all()

    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category,
        'description': c.description,
        'reviews': c.reviews
    } for c in results])


@app.route('/coffee/reviews')
def get_unique_reviews():
    """Список уникальных элементов в заметках к кофе."""
    # Получаем все reviews и находим уникальные
    all_reviews = db.session.query(Coffee.reviews).all()
    unique_reviews = set()

    for reviews_list in all_reviews:
        if reviews_list[0]:
            unique_reviews.update(reviews_list[0])

    return jsonify(list(unique_reviews))


@app.route('/users/by-country')
def get_users_by_country():
    """Список пользователей, проживающих в стране."""
    country = request.args.get('country', '')

    users = User.query.filter(
        text("address->>'country' = :country").bindparams(country=country)
    ).all()

    return jsonify([{
        'id': u.id,
        'name': u.name,
        'address': u.address,
        'coffee_id': u.coffee_id
    } for u in users])


@app.route('/coffee')
def get_coffee_list():
    """Список всего кофе."""
    coffee_list = Coffee.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category,
        'description': c.description,
        'reviews': c.reviews
    } for c in coffee_list])


@app.route('/users/list')
def get_users_list():
    """Список всех пользователей."""
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'has_sale': u.has_sale,
        'address': u.address,
        'coffee_id': u.coffee_id
    } for u in users])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
