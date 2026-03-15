import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

CREATE_USER_TABLE = """
DROP TABLE IF EXISTS 'user';
CREATE TABLE 'user' (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    email TEXT VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL
) 
"""

CREATE_POST_TABLE = """
DROP TABLE IF EXISTS 'post';
CREATE TABLE 'post' (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author INTEGER NOT NULL REFERENCES user(user_id),
    content TEXT NOT NULL DEFAULT ''
);
"""

CREATE_TABLE_LIKE = """
DROP TABLE IF EXISTS 'like';
CREATE TABLE 'like' (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (user_id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE 
)
"""


def create_tables() -> None:
    with sqlite3.connect("surrogate.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.executescript(CREATE_USER_TABLE)
        cursor.executescript(CREATE_POST_TABLE)
        cursor.executescript(CREATE_TABLE_LIKE)


def insert_sample_data() -> None:
    with sqlite3.connect("surrogate.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)", ('user1', 'user1@example.com', 'First1'))
        user1_id = cursor.lastrowid
        cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)", ('user2', 'user2@example.com', 'First2'))
        user2_id = cursor.lastrowid
        cursor.execute("INSERT INTO post (author, content) VALUES (?, ?)", (user1_id, 'Hello world'))
        cursor.execute("INSERT INTO post (author, content) VALUES (?, ?)", (user2_id, 'Nice to meet you'))
        cursor.execute("INSERT INTO post (author, content) VALUES (?, ?)", (user1_id, 'Second post'))
        # Insert likes
        cursor.execute("INSERT INTO \"like\" (user_id, post_id) VALUES (?, ?)", (user1_id, 1))  # user1 likes post 1
        cursor.execute("INSERT INTO \"like\" (user_id, post_id) VALUES (?, ?)", (user2_id, 2))  # user2 likes post 2


if __name__ == '__main__':
    create_tables()
    insert_sample_data()
