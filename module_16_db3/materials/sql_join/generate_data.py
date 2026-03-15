import sqlite3

CREATE_TABLE_1 = """
DROP TABLE IF EXISTS 'table_1';
CREATE TABLE 'table_1' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    born_city VARCHAR(255) NOT NULL
)
"""

CREATE_TABLE_2 = """
DROP TABLE IF EXISTS 'table_2';
CREATE TABLE 'table_2' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    born_country VARCHAR(255) NOT NULL
)
"""

TABLE_1_DATA = [
    ('John', 'Smith', 20, 'Beijing'),
    ('John', 'Ivanovich', 50, 'Rhaden'),
    ('Miles', 'Lang', 20, 'Moscow'),
    ('Bertram', 'Haley', 37, 'Warsaw'),
    ('Kwame', 'Petty', 23, 'Paris'),
    ('Simrah', 'Valenzuela', 26, 'Londow'),
    ('Fabien', 'Clay', 30, 'Berlin'),
    ('Dante', 'Donnelly', 50, 'Munich'),
    ('Hussein', 'Hagan', 10, 'Omsk'),
]

TABLE_2_DATA = [
    ('John', 'Smith', 20, 'China'),
    ('Miles', 'Smith', 21, 'USA'),
    ('Mairead', 'Mcnally', 32, 'Beijing'),
    ('Remy', 'Grant', 38, 'India'),
    ('Hawa', 'Campos', 99, 'Japan'),
    ('Denny', 'Sanderson', 12, 'Russia'),
    ('Humza', 'Owens', 50, 'Polland'),
    ('Burhan', 'John', 10, 'Holland'),
]


def create_tables() -> None:
    with sqlite3.connect("sql_join_tables.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(CREATE_TABLE_1)
        cursor.executescript(CREATE_TABLE_2)
        cursor.executemany(
            """
            INSERT INTO 'table_1'(first_name, last_name, age, born_city)
            VALUES (?, ?, ?, ?)
            """,
            TABLE_1_DATA
        )
        cursor.executemany(
            """
            INSERT INTO 'table_2'(first_name, last_name, age, born_country)
            VALUES (?, ?, ?, ?)
            """,
            TABLE_2_DATA
        )


if __name__ == '__main__':
    create_tables()
