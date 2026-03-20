from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import get_book_by_title, get_author_by_id, Book


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)
    author = fields.Str(dump_only=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author_id')
    def validate_author_id(self, author_id: int) -> None:
        if get_author_by_id(author_id) is None:
            raise ValidationError(
                'Author with id "{author_id}" does not exist.'.format(author_id=author_id)
            )

    @post_load
    def create_book(self, data: dict) -> Book:
        book = Book(title=data['title'], author_id=data['author_id'])
        author = get_author_by_id(data['author_id'])
        if author:
            book.author = f"{author.first_name} {author.middle_name or ''} {author.last_name}".strip()
        return book
