# Домашнее задание 3: Docker + PostgreSQL + Flask + Alembic

## Структура проекта

```
hw3/
├── docker-compose.yml      # Задание 1: Docker-контейнеры
├── Dockerfile              # Сборка Flask-приложения
├── requirements.txt        # Зависимости
├── app.py                  # Задание 2: Flask-приложение с SQLAlchemy
├── alembic.ini             # Конфигурация Alembic
├── alembic/                # Директория миграций (Задание 3)
│   ├── env.py
│   ├── script.py.mako
│   ├── README
│   └── versions/
│       ├── 001_init_migration.py    # Init миграция
│       ├── 002_remove_has_sale.py   # Удаление has_sale
│       ├── 004_add_surname.py       # Добавление surname
│       └── 005_add_patronymic.py    # Конфликтная миграция
└── README.md               # Этот файл
```

## Задание 1: Docker-контейнеры

### Запуск

```bash
docker-compose up -d
```

### Описание сервисов

**flask_app**: Flask-приложение с Gunicorn
- Порт: 8000
- Зависимость: postgres_db
- Сеть: app_network

**postgres_db**: PostgreSQL с кастомными настройками логирования
- Порт: 5432
- Настройки:
  - `log_destination=stderr` — логи в stderr
  - `logging_collector=on` — сборщик логов включён
  - `log_directory=/var/log/postgresql` — директория для логов
- Volumes:
  - `postgres_data` — данные БД
  - `postgres_logs` — логи PostgreSQL

## Задание 2: Работа с PostgreSQL

### Инициализация базы данных

```bash
# Подключение к PostgreSQL и создание БД
docker exec -it postgres_skillbox psql -U skillbox_user -c "CREATE DATABASE skillbox_db;"

# Или через psql на хосте (после экспорта порта)
psql -h localhost -U skillbox_user -c "CREATE DATABASE skillbox_db;"
```

### Создание таблиц через psql

```bash
psql -h localhost -U skillbox_user -d skillbox_db

-- Создание таблицы coffee
CREATE TABLE coffee (
    id SERIAL NOT NULL,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(200),
    description VARCHAR(200),
    reviews VARCHAR[],
    PRIMARY KEY (id)
);

-- Создание таблицы users
CREATE TABLE users (
    id SERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    has_sale BOOLEAN,
    address JSON,
    coffee_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(coffee_id) REFERENCES coffee (id)
);
```

### API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/users` | Добавление пользователя |
| GET | `/coffee/search?title=...` | Полнотекстовый поиск кофе |
| GET | `/coffee/reviews` | Уникальные отзывы о кофе |
| GET | `/users/by-country?country=...` | Пользователи по стране |
| GET | `/coffee` | Список кофе |
| GET | `/users/list` | Список пользователей |

### Пример использования

```bash
# Добавление пользователя
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "coffee_id": 1, "address": {"country": "USA", "city": "NY"}}'

# Поиск кофе
curl "http://localhost:8000/coffee/search?title=espresso"

# Пользователи по стране
curl "http://localhost:8000/users/by-country?country=USA"

# Уникальные отзывы
curl "http://localhost:8000/coffee/reviews"
```

## Задание 3: Работа с миграциями

### Команды Alembic

```bash
# Инициализация Alembic (уже выполнено)
alembic init alembic

# П. 2: Создание init-миграции (уже создана: 001_init_migration.py)
alembic revision -m "Initial migration"

# Накатить init-миграцию
alembic upgrade 001_init_migration

# П. 3: Создание миграции по удалению has_sale (уже создана: 002_remove_has_sale.py)
alembic revision -m "Remove has_sale"

# Накатить миграцию
alembic upgrade 002_remove_has_sale

# П. 4: Откатить миграцию (вернуть has_sale)
alembic downgrade 001_init_migration

# П. 5: Создание миграции по добавлению surname (уже создана: 004_add_surname.py)
alembic revision -m "Add surname"

# Накатить
alembic upgrade 004_add_surname

# П. 6: Конфликтная миграция с неправильным down_revision
# Уже создана: 005_add_patronymic.py с down_revision = '001_init_migration'

# П. 7: Попытка накатить вызовет MultipleHeads ошибку
alembic upgrade head

# Решение конфликта — merge миграция
alembic merge 004_add_surname 005_add_patronymic -m "Merge branches"

# Или ручное исправление down_revision в 005_add_patronymic.py
```

### Решение конфликта миграций

Конфликт возникает, когда две миграции имеют одинаковый `down_revision`. 

**Вариант 1: Merge миграция**
```bash
alembic merge 004_add_surname 005_add_patronymic -m "Merge heads"
```

**Вариант 2: Исправление down_revision**
В файле `005_add_patronymic.py` изменить:
```python
down_revision = '004_add_surname'  # Вместо '001_init_migration'
```

Затем накатить:
```bash
alembic upgrade head
```

## Специальные типы данных PostgreSQL

### ARRAY (массив отзывов о кофе)
```python
from sqlalchemy.dialects.postgresql import ARRAY

reviews = db.Column(ARRAY(db.String))
```

### JSON (адрес пользователя)
```python
from sqlalchemy.dialects.postgresql import JSON

address = db.Column(JSON)

# Поиск по JSON
User.query.filter(text("address->>'country' = :country").bindparams(country='USA'))
```

### Полнотекстовый поиск
```python
db.session.query(Coffee).filter(
    text("to_tsvector('english', title) @@ plainto_tsquery('english', :query)").bindparams(query=title)
)
```
