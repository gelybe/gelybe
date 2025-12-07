import unittest
from datetime import datetime
from person import Person


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = Person("Иван", 1990, "ул. Пушкина, 10")

    def test_init(self):
        self.assertEqual(self.person.name, "Иван")
        self.assertEqual(self.person.yob, 1990)
        self.assertEqual(self.person.address, "ул. Пушкина, 10")

    def test_get_age(self):
        current_year = datetime.now().year
        expected_age = current_year - 1990
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Иван")

    def test_set_name(self):
        self.person.set_name("Пётр")
        self.assertEqual(self.person.get_name(), "Пётр")

    def test_set_address(self):
        self.person.set_address("ул. Ленина, 5")
        self.assertEqual(self.person.get_address(), "ул. Ленина, 5")

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), "ул. Пушкина, 10")  # Исправлено

    def test_is_homeless_with_address(self):
        self.assertFalse(self.person.is_homeless())

    def test_is_homeless_without_address(self):
        person_without_address = Person("Анна", 2000)
        self.assertTrue(person_without_address.is_homeless())

    def test_is_homeless_with_empty_string(self):
        person_empty_address = Person("Мария", 1985, "")
        self.assertTrue(person_empty_address.is_homeless())


if __name__ == '__main__':
    unittest.main()
