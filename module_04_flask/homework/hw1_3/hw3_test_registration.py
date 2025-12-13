"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app,
class TestRegistrationForm(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Тест для поля email

    def test_email_valid(self):
        """Положительный кейс: корректный email"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered', response.get_data(as_text=True))


    def test_email_invalid(self):
        """Отрицательный кейс: некорректный email"""
        data = {
            'email': 'invalid-email',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.get_data(as_text=True))
        self.assertIn('Invalid email address', response.get_data(as_text=True))

    # Тест для поля phone

    def test_phone_valid(self):
        """Положительный кейс: корректный телефон (11 цифр)"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('+791234567890', response.get_data(as_text=True))


    def test_phone_too_short(self):
        """Отрицательный кейс: телефон короче 10 цифр"""
        data = {
            'email': 'user@example.com',
            'phone': 123456789,  # 9 цифр
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.get_data(as_text=True))
        self.assertIn('Number must be between 1000000000 and 99999999999', response.get_data(as_text=True))


    def test_phone_too_long(self):
        """Отрицательный кейс: телефон длиннее 11 цифр"""
        data = {
            'email': 'user@example.com',
            'phone': 123456789012,  # 12 цифр
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.get_data(as_text=True))
        self.assertIn('Number must be between 1000000000 and 99999999999', response.get_data(as_text=True))

    # Тест для поля name

    def test_name_valid(self):
        """Положительный кейс: корректное имя"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Иван Иванов', response.get_data(as_text=True))


    def test_name_empty(self):
        """Отрицательный кейс: пустое имя"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': '',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.get_data(as_text=True))
        self.assertIn('This field is required', response.get_data(as_text=True))


    # Тест для поля address
    def test_address_valid(self):
        """Положительный кейс: корректный адрес"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ул. Примерная, 1', response.get_data(as_text=True))


    def test_address_empty(self):
        """Отрицательный кейс: пустой адрес"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': '',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('address', response.get_data(as_text=True))
        self.assertIn('This field is required', response.get_data(as_text=True))


    # Тест для поля index
    def test_index_valid(self):
        """Положительный кейс: корректный индекс (6 цифр)"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('123456', response.get_data(as_text=True))


    def test_index_too_short(self):
        """Отрицательный кейс: индекс короче 6 цифр"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 12345  # 5 цифр
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('index', response.get_data(as_text=True))
        self.assertIn('Number must be between 100000 and 999999', response.get_data(as_text=True))


    def test_index_too_long(self):
        """Отрицательный кейс: индекс длиннее 6 цифр"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 1234567  # 7 цифр
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('index', response.get_data(as_text=True))
        self.assertIn('Number must be between 100000 and 999999', response.get_data(as_text=True))


    # Тест для поля comment (необязательное поле)
    def test_comment_optional(self):
        """Положительный кейс: поле comment может быть пустым"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456,
            'comment': ''  # пустое значение
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered', response.get_data(as_text=True))


    def test_comment_with_value(self):
        """Положительный кейс: поле comment заполнено"""
        data = {
            'email': 'user@example.com',
            'phone': 91234567890,
            'name': 'Иван Иванов',
            'address': 'ул. Примерная, 1',
            'index': 123456,
            'comment': 'Оставьте у двери'
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Оставьте у двери', response.get_data(as_text=True))


    # Дополнительный негативный тест: отсутствие обязательных полей
    def test_missing_required_fields(self):
        """Отрицательный кейс: отсутствуют обязательные поля"""
        data = {
            'email': '',  # обязательно
            'phone': '',  # обязательно
            'name': '',  # обязательно
            'address': '',  # обязательно
            'index': ''  # обязательно
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)

        # Проверяем, что все обязательные поля присутствуют в ошибках
        error_text = response.get_data(as_text=True)
        self.assertIn('email', error_text)
        self.assertIn('phone', error_text)
        self.assertIn('name', error_text)
        self.assertIn('address', error_text)
        self.assertIn('index', error_text)


if __name__ == '__main__':
    unittest.main()
