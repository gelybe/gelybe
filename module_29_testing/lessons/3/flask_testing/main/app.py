from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///prod.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Product, User

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/test_route")
    def math_route():
        """Тестовый роут для расчета степени"""
        number = int(request.args.get("number", 0))
        result = number ** 2
        return jsonify(result)

    @app.route("/users", methods=['POST'])
    def create_user_handler():
        """Создание нового пользователя"""
        name = request.form.get('name', type=str)
        email = request.form.get('email', type=str)
        surname = request.form.get('surname', type=str)

        new_user = User(name=name,
                        surname=surname,
                        email=email)

        db.session.add(new_user)
        db.session.commit()

        return '', 201

    @app.route("/users", methods=['GET'])
    def get_users_handler():
        """Получение пользователей"""
        users: List[User] = db.session.query(User).all()
        users_list = [u.to_json() for u in users]
        return jsonify(users_list), 200

    @app.route("/users/<int:user_id>", methods=['GET'])
    def get_user_handler(user_id: int):
        """Получение пользователя по ид"""
        user: User = db.session.query(User).get(user_id)
        return jsonify(user.to_json()), 200

    @app.route("/products", methods=['POST'])
    def create_product_handler():
        """Создание нового продукта пользователя"""
        title = request.form.get('title', type=str)
        price = request.form.get('price', type=float)
        user_id = request.form.get('user_id', type=int)

        new_product = Product(title=title,
                              price=price,
                              user_id=user_id)

        db.session.add(new_product)
        db.session.commit()
        return '', 201

    @app.route("/products/<int:product_id>", methods=['PATCH'])
    def update_product_handler(product_id: int):
        """
        Изменение продукта
        """
        title = request.form.get('title', type=str)
        price = request.form.get('price', type=float)
        user_id = request.form.get('user_id', type=int)

        product = db.session.query(Product).get(product_id)
        if title:
            product.title = title
        if price:
            product.price = price
        if user_id:
            product.user_id = user_id

        db.session.commit()
        return '', 201

    @app.route("/", methods=['GET'])
    def get_template_handler() -> str:
        """Получение UI-интерфейса с продуктами от пользователей"""

        products = db.session.query(Product).all()
        products_by_users = []
        for p in products:
            product_obj = dict(**p.to_json(),
                               user=p.user.to_json())
            products_by_users.append(product_obj)
        return render_template("user_products.html",
                               products=products_by_users)

    return app
