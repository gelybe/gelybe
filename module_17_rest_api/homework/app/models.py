import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Book:
    title: str
    author_id: int
    author: Optional[str] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)

def parse_author(name: str) -> Author:
    parts = name.split()
    if len(parts) == 1:
        return Author(first_name=parts[0], last_name='', middle_name=None)
    elif len(parts) == 2:
        first, last = parts
        return Author(first_name=first, last_name=last, middle_name=None)
    else:
        first = parts[0]
        last = parts[-1]
        middle = ' '.join(parts[1:-1])
        return Author(first_name=first, last_name=last, middle_name=middle)

def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])

def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        # Create authors table if not exists
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT
            );
            """
        )
        # Insert unique authors
        for item in initial_records:
            author_name = item['author']
            # Check if author exists
            cursor.execute(
                f"""
                SELECT id FROM `{AUTHORS_TABLE_NAME}` WHERE first_name || COALESCE(' ' || middle_name, '') || ' ' || last_name = ?
                """,
                (author_name,)
            )
            if not cursor.fetchone():
                author = parse_author(author_name)
                cursor.execute(
                    f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name, middle_name) VALUES (?, ?, ?)
                    """,
                    (author.first_name, author.last_name, author.middle_name)
                )
        # Create books table if not exists
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES `{AUTHORS_TABLE_NAME}`(id) ON DELETE CASCADE
            );
            """
        )
        # Insert books if not exist
        for item in initial_records:
            cursor.execute(
                f"""
                SELECT id FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
                """,
                (item['title'],)
            )
            if not cursor.fetchone():
                # find author_id
                author_name = item['author']
                cursor.execute(
                    f"""
                    SELECT id FROM `{AUTHORS_TABLE_NAME}` WHERE first_name || COALESCE(' ' || middle_name, '') || ' ' || last_name = ?
                    """,
                    (author_name,)
                )
                author_id = cursor.fetchone()[0]
                cursor.execute(
                    f"""
                    INSERT INTO `{BOOKS_TABLE_NAME}`
                    (title, author_id) VALUES (?, ?)
                    """,
                    (item['title'], author_id)
                )


def _get_book_obj_from_row(row: tuple) -> Book:
    author_name = f"{row[3]} {row[5] or ''} {row[4]}".strip()
    return Book(id=row[0], title=row[1], author_id=row[2], author=author_name)


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT b.id, b.title, b.author_id, a.first_name, a.last_name, a.middle_name FROM `{BOOKS_TABLE_NAME}` b JOIN `{AUTHORS_TABLE_NAME}` a ON b.author_id = a.id')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        # set author name
        author = get_author_by_id(book.author_id)
        if author:
            book.author = f"{author.first_name} {author.middle_name or ''} {author.last_name}".strip()
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT b.id, b.title, b.author_id, a.first_name, a.last_name, a.middle_name FROM `{BOOKS_TABLE_NAME}` b JOIN `{AUTHORS_TABLE_NAME}` a ON b.author_id = a.id WHERE b.id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()
        # update author name if needed
        author = get_author_by_id(book.author_id)
        if author:
            book.author = f"{author.first_name} {author.middle_name or ''} {author.last_name}".strip()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT b.id, b.title, b.author_id, a.first_name, a.last_name, a.middle_name FROM `{BOOKS_TABLE_NAME}` b JOIN `{AUTHORS_TABLE_NAME}` a ON b.author_id = a.id WHERE b.title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT id, first_name, last_name, middle_name FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )
        row = cursor.fetchone()
        if row:
            return _get_author_obj_from_row(row)
