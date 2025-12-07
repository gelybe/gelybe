import unittest
import sys
import os

# Добавляем путь к основному приложению
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, storage


class TestFinanceApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Инициализация тестовых данных перед всеми тестами."""
        cls.original_data = {
            '20230101': 100,
            '20230102': 200,
            '20230103': -50,
            '20230215': 300,
            '20230220': -100
        }

    def setUp(self):
        """Настройка тестового клиента и данных перед каждым тестом."""
        self.app = app.test_client()
        self.app.testing = True
        # Очищаем и восстанавливаем storage перед каждым тестом
        storage.clear()
        storage.update(self.__class__.original_data)

    def tearDown(self):
        """Очистка storage после каждого теста."""
        storage.clear()

    # === Тесты для /add/ ===

    def test_add_valid_entry(self):
        """Проверка успешного добавления записи."""
        response = self.app.post('/add/20230110/150')
        self.assertEqual(response.status_code, 200)
        self.assertIn('добавлена', response.get_data(as_text=True))
        self.assertIn('20230110', storage)
        self.assertEqual(storage['20230110'], 150)

    def test_add_negative_amount(self):
        """Проверка добавления отрицательной суммы (расход)."""
        response = self.app.post('/add/20230111/-50')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage['20230111'], -50)

    def test_add_invalid_date_format_returns_404(self):
        """Проверка, что /add/ отклоняет невалидный формат даты (не YYYYMMDD)."""
        response = self.app.post('/add/2023/01/01/100')
        self.assertEqual(response.status_code, 404)

        response = self.app.post('/add/01012023/100')
        self.assertEqual(response.status_code, 404)

    # === Тесты для /calculate/ (без параметра) ===

    def test_calculate_total_balance(self):
        """Проверка расчёта общего баланса."""
        response = self.app.get('/calculate/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('450', response.get_data(as_text=True))

    def test_calculate_total_empty_storage(self):
        """Проверка расчёта общего баланса при пустом хранилище."""
        storage.clear()
        response = self.app.get('/calculate/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('0', response.get_data(as_text=True))

    def test_calculate_total_with_zero_balance(self):
        """Проверка расчёта, если все суммы компенсируют друг друга."""
        storage.clear()
        storage.update({'20230101': 100, '20230102': -100})
        response = self.app.get('/calculate/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('0', response.get_data(as_text=True))

    # === Тесты для /calculate/<year> ===

    def test_calculate_year_balance(self):
        """Проверка расчёта баланса за конкретный год."""
        response = self.app.get('/calculate/2023')
        self.assertEqual(response.status_code, 200)
        self.assertIn('450', response.get_data(as_text=True))

    def test_calculate_nonexistent_year_returns_zero(self):
        """Проверка расчёта за год, которого нет в данных."""
        response = self.app.get('/calculate/2022')
        self.assertEqual(response.status_code, 200)
        self.assertIn('0', response.get_data(as_text=True))

    def test_calculate_year_with_partial_data(self):
        """Проверка расчёта за год с существующими данными."""
        response = self.app.get('/calculate/2023')
        self.assertEqual(response.status_code, 200)
        self.assertIn('450', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()