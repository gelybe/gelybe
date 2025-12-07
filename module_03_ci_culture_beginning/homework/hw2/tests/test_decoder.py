import unittest
import sys
import os

# Добавляем папку hw2 в путь для импорта модуля decrypt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decrypt import decode


class TestDecoder(unittest.TestCase):
    """Набор тестов для функции decode, проверяющей логику дешифрования строк."""

    def test_no_dots(self):
        """Тест: строка без точек — возвращается без изменений."""
        self.assertEqual(decode('абра-кадабра'), 'абра-кадабра')

    def test_single_dot_removes_last_char(self):
        """Тест: одна точка удаляет один символ."""
        # 'абра-кадабра.' -> убираем точку и последний символ 'а' -> 'абра-кадабр'
        self.assertEqual(decode('абра-кадабра.'), 'абра-кадабр')

    def test_two_dots_remove_one_char(self):
        """Тест: две точки — удаляется один предыдущий символ."""
        cases = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decode(encrypted), expected)

    def test_multiple_dots_sequential_removal(self):
        """Тест: три и более точек — удаляется по одному символу на каждую точку."""
        cases = [
            ('абраа..-.кадабра', 'абра-кадабра'),  # 3 точки: удаляем 3 символа
            ('абрау...-кадабра', 'абра-кадабра'),  # 3 точки
            ('абр......a.', 'a'),                   # 7 точек и одна в конце
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decode(encrypted), expected)

    def test_only_dots(self):
        """Тест: строка состоит только из точек — результат пустой."""
        cases = [
            ('.', ''),
            ('........', ''),
            ('1.......................', ''),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decode(encrypted), expected)

    def test_mixed_digits_and_dots(self):
        """Тест: комбинации цифр и точек."""
        cases = [
            ('1..2.3', '23'),
            ('1...2', '2'),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decode(encrypted), expected)

    def test_empty_string(self):
        """Тест: пустая строка."""
        self.assertEqual(decode(''), '')


if __name__ == '__main__':
    unittest.main()