from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta

# SQL-запросы создания таблиц
# таблица книг в библиотеке
books = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    count INTEGER DEFAULT 1,
    release_date DATE NOT NULL,
    author_id INTEGER NOT NULL
)
"""

# таблица авторов
authors = """
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL
)
"""

# таблица читателей
students = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    average_score FLOAT NOT NULL,
    scholarship BOOLEAN NOT NULL
)
"""

# таблица выдачи книг студентам
receiving_books = """
CREATE TABLE IF NOT EXISTS receiving_books (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    date_of_issue DATETIME NOT NULL,
    date_of_return DATETIME
)
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    count = db.Column(db.Integer, default=1)
    release_date = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    scholarship = db.Column(db.Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls):
        return cls.query.filter(cls.scholarship == True).all()

    @classmethod
    def get_students_with_score_higher_than(cls, score):
        return cls.query.filter(cls.average_score > score).all()

class ReceivingBook(db.Model):
    __tablename__ = 'receiving_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_of_return = db.Column(db.DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.utcnow() - self.date_of_issue).days

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': book.release_date.isoformat(),
            'author_id': book.author_id
        })
    return jsonify(result)

@app.route('/debtors', methods=['GET'])
def get_debtors():
    today = datetime.utcnow()
    two_weeks_ago = today - timedelta(days=14)
    debtors = ReceivingBook.query.filter(
        ReceivingBook.date_of_return.is_(None),
        ReceivingBook.date_of_issue <= two_weeks_ago
    ).all()
    result = []
    for debtor in debtors:
        student = Student.query.get(debtor.student_id)
        book = Book.query.get(debtor.book_id)
        result.append({
            'student_name': f"{student.name} {student.surname}",
            'book_name': book.name,
            'days_with_book': debtor.count_date_with_book
        })
    return jsonify(result)

@app.route('/issue-book', methods=['POST'])
def issue_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Missing book_id or student_id'}), 400

    existing_record = ReceivingBook.query.filter_by(
        book_id=book_id,
        student_id=student_id,
        date_of_return=None
    ).first()

    if existing_record:
        return jsonify({'error': 'Book already issued to this student'}), 400

    new_record = ReceivingBook(book_id=book_id, student_id=student_id)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Book issued successfully'}), 201

@app.route('/return-book', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    record = ReceivingBook.query.filter_by(
        book_id=book_id,
        student_id=student_id,
        date_of_return=None
    ).first()

    if not record:
        return jsonify({'error': 'No such book issuance record found'}), 404

    record.date_of_return = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200

@app.route('/search-books', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    books = Book.query.filter(Book.name.ilike(f'%{query}%')).all()
    result = []
    for book in books:
        author = Author.query.get(book.author_id)
        result.append({
            'id': book.id,
            'name': book.name,
            'author': f"{author.name} {author.surname}" if author else 'Unknown',
            'release_date': book.release_date.isoformat()
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
