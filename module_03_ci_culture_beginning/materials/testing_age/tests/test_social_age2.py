import unittest
import sys
import os

# Добавляем корневую папку в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from social_age import get_social_status


class TestSocialAge(unittest.TestCase):
    # Позитивные тесты
    def test_child_age(self):
        self.assertEqual(get_social_status(8), 'ребенок')

    def test_teenager_age(self):
        self.assertEqual(get_social_status(15), 'подросток')

    def test_adult_age(self):
        self.assertEqual(get_social_status(30), 'взрослый')

    def test_elderly_age(self):
        self.assertEqual(get_social_status(55), 'пожилой')

    def test_pensioner_age(self):
        self.assertEqual(get_social_status(70), 'пенсионер')

    # Негативные тесты
    def test_negative_age(self):
        with self.assertRaises(ValueError):
            get_social_status(-5)

    def test_string_age(self):
        with self.assertRaises(ValueError):
            get_social_status("old")

    def test_none_age(self):
        with self.assertRaises(ValueError):
            get_social_status(None)

    def test_list_age(self):
        with self.assertRaises(ValueError):
            get_social_status([1, 2, 3])

    def test_dict_age(self):
        with self.assertRaises(ValueError):
            get_social_status({"age": 25})

    # Этот тест не будет запускаться, так как не начинается с 'test'
    def check_can_get_adult_status(self):
        self.assertEqual(get_social_status(25), 'взрослый')

    # Этот тест будет запускаться, так как начинается с 'test', даже с CamelCase
    def testGetSeniorAge(self):
        self.assertEqual(get_social_status(80), 'пенсионер')


if __name__ == '__main__':
    unittest.main()