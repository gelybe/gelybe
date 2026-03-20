from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
)
from schemas import BookSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book_data = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = Book(title=book_data['title'], author_id=book_data['author_id'])
        book = add_book(book)
        return schema.dump(book), 201


api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
