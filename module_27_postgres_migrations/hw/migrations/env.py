from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os
import sys

# Добавляем корень проекта в PYTHONPATH, чтобы можно было импортировать `app`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем Flask-приложение и объект базы данных
from app import app, db

# Получаем конфигурацию Alembic из alembic.ini
config = context.config

# Настройка логирования из файла (если указано в alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные для генерации миграций
target_metadata = db.Model.metadata

def get_url():
    """Возвращает URL базы данных из переменной окружения или использует значение по умолчанию."""
    return os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg://skillbox_user:skillbox_pass@localhost:5432/skillbox_db'
    )

def run_migrations_offline():
    """Запуск миграций в offline-режиме (без подключения к БД)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в online-режиме (с подключением к реальной БД)."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Определяем, в каком режиме запускать миграции
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()