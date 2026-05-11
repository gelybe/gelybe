from sqlalchemy import Column, Integer, String, Float, \
    create_engine, Sequence, Identity, ForeignKey, delete
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask import Flask, jsonify
from typing import Dict, Any

app = Flask(__name__)
engine = create_engine('sqlite:///app.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    count = Column(Integer, default=0)
    price = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="products")

    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    num = Column(Integer, default=100)

    def __repr__(self):
        return f"Пользователь {self.username}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


@app.before_request
def before_request_func():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    objects = [
        User(name='u1'),
        User(name='u2'),
        User(name='u3'),
        Product(title="p1", user_id=1),
        Product(title="p2", user_id=2),
        Product(title="p3", user_id=3)
    ]
    session.bulk_save_objects(objects)
    session.commit()


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product_handler(id: int):
    result = delete(Product).returning(Product.id, Product.title). \
        where(Product.id == id)
    deleted_row = session.execute(result).fetchone()
    if deleted_row:
        deleted_row_json = dict(id=deleted_row[0], title=deleted_row[1])
        return jsonify(delete_row_attrs=deleted_row_json)


@app.route('/products', methods=['POST'])
def insert_product_handler():
    # SQLite версия - простая вставка
    new_product = Product(id=2, title='новый продукт')
    session.add(new_product)
    session.commit()
    return '', 200


@app.route('/products', methods=['GET'])
def get_products_handler():
    products = session.query(Product).all()
    products_list = []
    for p in products:
        product_obj = p.to_json()
        product_obj['user'] = p.user.to_json()
        products_list.append(product_obj)
    return jsonify(products_list)


if __name__ == '__main__':
    app.run()
