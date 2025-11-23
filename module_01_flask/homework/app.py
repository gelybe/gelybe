import datetime
import os
import re
import random
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

# Глобальные списки — не пересоздаются при каждом запросе
CARS = ["Chevrolet", "Renault", "Ford", "Lada"]
CATS = [
    "корниш-рекс",
    "русская голубая",
    "шотландская вислоухая",
    "мейн-кун",
    "манчкин",
]

# Загрузка слов из книги один раз при запуске приложения
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
WORDS = []
try:
    with open(BOOK_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
        # Извлекаем слова (русские и латинские буквы)
        WORDS = re.findall(r"[A-Za-zА-Яа-яЁё]+", text, flags=re.UNICODE)
except FileNotFoundError:
    # Если файл не найден — оставляем WORDS пустым
    WORDS = []


@app.route('/hello_world')
def hello_world():
    """Задача 1: страница с текстом «Привет, мир!»"""
    return "Привет, мир!"


@app.route('/cars')
def cars():
    """Задача 2: возвращает список машин через запятую. Список хранится глобально."""
    cars_list = ", ".join(CARS)
    return cars_list


@app.route('/cats')
def cats():
    """Задача 3: возвращает случайную породу из глобального списка."""
    chosen_cat = random.choice(CATS)
    return chosen_cat


@app.route('/get_time/now')
def get_time_now():
    """Задача 4: точное текущее время. Форматирование через переменные."""
    current_time = datetime.now()
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return f"Точное время: {current_time_str}"


@app.route('/get_time/future')
def get_time_future():
    """Задача 5: точное время через 1 час. Форматирование через переменные."""
    current_time = datetime.now()
    current_time_after_hour = current_time + timedelta(hours=1)
    current_time_after_hour_str = current_time_after_hour.strftime('%Y-%m-%d %H:%M:%S')
    return f"Точное время через час будет {current_time_after_hour_str}"


@app.route('/get_random_word')
def get_random_word():
    """Задача 6: случайное слово из war_and_peace.txt. Файл читается один раз при запуске."""
    if not WORDS:
        return "Файл war_and_peace.txt не найден или словарь пуст."
    random_word = random.choice(WORDS)
    return random_word


counter_visits = 0

@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return f'Страница открыта {counter_visits} раз'


if __name__ == '__main__':
    # Запуск для локальной разработки
    app.run(debug=True)

