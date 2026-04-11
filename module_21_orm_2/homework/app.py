from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref, joinedload, selectinload
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func, event
import re
import csv
from io import StringIO
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

    # Связь с книгами
    books = relationship('Book', backref='author', lazy='select')

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    count = db.Column(db.Integer, default=1)
    release_date = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    # Связь с выдачей книг
    receiving_books = relationship('ReceivingBook', backref='book', lazy='select', cascade='all, delete-orphan')
    # Связь многие-ко-многим с студентами через association_proxy
    students = association_proxy('receiving_books', 'student')

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    scholarship = db.Column(db.Boolean, nullable=False)

    # Связь с выдачей книг
    receiving_books = relationship('ReceivingBook', backref='student', lazy='select', cascade='all, delete-orphan')
    # Связь многие-ко-многим с книгами через association_proxy
    books = association_proxy('receiving_books', 'book')

    @classmethod
    def get_students_with_scholarship(cls):
        return cls.query.filter(cls.scholarship == True).all()

    @classmethod
    def get_students_with_score_higher_than(cls, score):
        return cls.query.filter(cls.average_score > score).all()

class ReceivingBook(db.Model):
    __tablename__ = 'receiving_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
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
    books = Book.query.options(joinedload(Book.author)).all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': book.release_date.isoformat(),
            'author': f"{book.author.name} {book.author.surname}"
        })
    return jsonify(result)

@app.route('/debtors', methods=['GET'])
def get_debtors():
    today = datetime.utcnow()
    two_weeks_ago = today - timedelta(days=14)
    debtors = ReceivingBook.query.filter(
        ReceivingBook.date_of_return.is_(None),
        ReceivingBook.date_of_issue <= two_weeks_ago
    ).options(joinedload(ReceivingBook.student), joinedload(ReceivingBook.book)).all()
    result = []
    for debtor in debtors:
        result.append({
            'student_name': f"{debtor.student.name} {debtor.student.surname}",
            'book_name': debtor.book.name,
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
    books = Book.query.options(joinedload(Book.author)).filter(Book.name.ilike(f'%{query}%')).all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'name': book.name,
            'author': f"{book.author.name} {book.author.surname}" if book.author else 'Unknown',
            'release_date': book.release_date.isoformat()
        })
    return jsonify(result)

# 1. Количество оставшихся в библиотеке книг по автору
@app.route('/books-by-author/<int:author_id>', methods=['GET'])
def get_books_by_author(author_id):
    author = Author.query.get_or_404(author_id)
    # Общее количество книг автора
    total_books = db.session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar() or 0
    # Количество выданных книг автора
    issued_books = ReceivingBook.query.join(Book).filter(
        Book.author_id == author_id,
        ReceivingBook.date_of_return.is_(None)
    ).count()
    available_books = max(total_books - issued_books, 0)
    return jsonify({
        'author': f"{author.name} {author.surname}",
        'available_books': available_books
    })

# 2. Список книг, которые студент не читал, но читал другие книги этого автора
@app.route('/unread-books-by-student/<int:student_id>', methods=['GET'])
def get_unread_books_by_student(student_id):
    student = Student.query.get_or_404(student_id)
    # Авторы, чьи книги читал студент
    authors_read = db.session.query(Author.id).join(Book).join(ReceivingBook).filter(
        ReceivingBook.student_id == student_id
    ).distinct()
    # Книги этих авторов, которые студент НЕ читал
    unread_books = Book.query.options(joinedload(Book.author)).join(Author).filter(
        Author.id.in_(authors_read),
        Book.id.not_in(
            db.session.query(ReceivingBook.book_id).filter(ReceivingBook.student_id == student_id)
        )
    ).all()
    result = []
    for book in unread_books:
        result.append({
            'id': book.id,
            'name': book.name,
            'author': f"{book.author.name} {book.author.surname}"
        })
    return jsonify(result)

# 3. Среднее количество книг, взятых студентами в этом месяце
@app.route('/average-books-this-month', methods=['GET'])
def get_average_books_this_month():
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Количество выдач в этом месяце
    issue_count = ReceivingBook.query.filter(ReceivingBook.date_of_issue >= start_of_month).count()
    # Количество уникальных студентов, бравших книги
    student_count = db.session.query(func.count(func.distinct(ReceivingBook.student_id))).filter(
        ReceivingBook.date_of_issue >= start_of_month
    ).scalar()
    average = issue_count / student_count if student_count > 0 else 0
    return jsonify({'average_books_per_student': round(average, 2)})

# 4. Самая популярная книга среди студентов со средним баллом > 4.0
@app.route('/most-popular-book-high-score', methods=['GET'])
def get_most_popular_book_high_score():
    high_score_students = db.session.query(Student.id).filter(Student.average_score > 4.0).subquery()
    popular_book = db.session.query(
        Book.id,
        Book.name,
        func.count(ReceivingBook.id).label('issue_count')
    ).join(ReceivingBook).filter(
        ReceivingBook.student_id.in_(high_score_students)
    ).group_by(Book.id).order_by(func.count(ReceivingBook.id).desc()).first()
    
    if popular_book:
        return jsonify({
            'book_id': popular_book.id,
            'book_name': popular_book.name,
            'issue_count': popular_book.issue_count
        })
    else:
        return jsonify({'message': 'No books found for high-score students'}), 404

# 5. ТОП-10 самых читающих студентов в этом году
@app.route('/top-10-readers-this-year', methods=['GET'])
def get_top_10_readers_this_year():
    start_of_year = datetime.utcnow().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    top_readers = db.session.query(
        Student.id,
        Student.name,
        Student.surname,
        func.count(ReceivingBook.id).label('books_count')
    ).join(ReceivingBook).filter(
        ReceivingBook.date_of_issue >= start_of_year
    ).group_by(Student.id).order_by(func.count(ReceivingBook.id).desc()).limit(10).all()
    
    result = []
    for reader in top_readers:
        result.append({
            'student_id': reader.id,
            'name': f"{reader.name} {reader.surname}",
            'books_count': reader.books_count
        })
    return jsonify(result)

# 6. Массовая вставка студентов из CSV
@app.route('/import-students-csv', methods=['POST'])
def import_students_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream, delimiter=';')
        students_data = []
        phone_pattern = re.compile(r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$')
        
        for row in csv_reader:
            # Валидация телефона
            if not phone_pattern.match(row['phone']):
                return jsonify({'error': f"Invalid phone format: {row['phone']}"}), 400
            students_data.append({
                'name': row['name'],
                'surname': row['surname'],
                'phone': row['phone'],
                'email': row['email'],
                'average_score': float(row['average_score']),
                'scholarship': row['scholarship'].lower() == 'true'
            })
        
        db.session.bulk_insert_mappings(Student, students_data)
        db.session.commit()
        return jsonify({'message': f'{len(students_data)} students imported successfully'}), 201
    
    return jsonify({'error': 'Invalid file format'}), 400

# 7. Валидация телефона перед вставкой
@event.listens_for(Student, 'before_insert')
def validate_phone_format(mapper, connection, target):
    phone_pattern = re.compile(r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$')
    if not phone_pattern.match(target.phone):
        raise ValueError(f"Phone number {target.phone} does not match format +7(9**)-***-**-**")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
