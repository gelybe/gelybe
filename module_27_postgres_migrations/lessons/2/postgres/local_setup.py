#!/usr/bin/env python3
"""
Скрипт для настройки локальной PostgreSQL базы данных
"""
import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Создание базы данных и пользователя"""
    try:
        # Подключение к PostgreSQL по умолчанию
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",  # Стандартный пароль при установке
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Создание пользователя
        try:
            cursor.execute("CREATE USER admin WITH PASSWORD 'admin'")
            print("✅ Пользователь 'admin' создан")
        except psycopg2.errors.DuplicateObject:
            print("ℹ️  Пользователь 'admin' уже существует")
        
        # Создание базы данных
        try:
            cursor.execute("CREATE DATABASE postgres_migrations OWNER admin")
            print("✅ База данных 'postgres_migrations' создана")
        except psycopg2.errors.DuplicateDatabase:
            print("ℹ️  База данных 'postgres_migrations' уже существует")
        
        # Предоставление прав
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE postgres_migrations TO admin")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Настройка завершена!")
        print("Подключение:")
        print("  Host: localhost")
        print("  Port: 5432")
        print("  Database: postgres_migrations")
        print("  User: admin")
        print("  Password: admin")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\nУбедитесь, что:")
        print("1. PostgreSQL установлен")
        print("2. Служба PostgreSQL запущена")
        print("3. Пароль для пользователя postgres корректен")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
