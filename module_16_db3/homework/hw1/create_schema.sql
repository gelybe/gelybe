-- Включение поддержки внешних ключей
PRAGMA foreign_keys = ON;

-- Удаление таблиц, если они существуют
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS Hall;
DROP TABLE IF EXISTS cinema;

-- Таблица залов
CREATE TABLE hall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cinema_id INTEGER NOT NULL,
    FOREIGN KEY (cinema_id) REFERENCES cinema(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица фильмов
CREATE TABLE movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    duration INTEGER NOT NULL CHECK (duration > 0)
);

-- Таблица сеансов
CREATE TABLE session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    start_time TEXT NOT NULL, -- формат: 'YYYY-MM-DD HH:MM'
    price REAL NOT NULL CHECK (price >= 0),
    FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES hall(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Таблица бронирований
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    seat_row INTEGER NOT NULL CHECK (seat_row >= 1),
    seat_number INTEGER NOT NULL CHECK (seat_number >= 1),
    FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (session_id, seat_row, seat_number)
);