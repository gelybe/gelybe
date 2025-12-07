from freezegun import freeze_time
import sys
import os

# Добавляем папку hw1 в путь, чтобы импортировать модуль
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_world_with_day import hello_world


def test_can_get_correct_weekday_in_response():
    """
    Проверяет, что возвращаемое приветствие содержит правильный день недели,
    независимо от переданного имени (включая пожелания вроде 'Хорошей среды').
    Тестируются все 7 дней недели с использованием freeze_time.
    """
    weekday_map = {
        0: 'понедельника',
        1: 'вторника',
        2: 'среды',
        3: 'четверга',
        4: 'пятницы',
        5: 'субботы',
        6: 'воскресенья'
    }

    # Тестируем каждый день недели
    for day_index, expected_day in weekday_map.items():
        # Выбираем дату: 2023-01-02 — понедельник, далее + day_index
        fake_date = f"2023-01-{day_index + 2:02d}"

        with freeze_time(fake_date):
            # Передаём имя, которое может вводить в заблуждение
            username = "Пользователь Хорошей среды"
            result = hello_world(username)

            # Проверяем, что в ответе используется правильный день недели
            assert expected_day in result, (
                f"Ожидался день недели: {expected_day}, но ответ: {result}"
            )