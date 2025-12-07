import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from social_age import get_social_status


class TestSocialAge(unittest.TestCase):
    def test_can_get_child_age(self):
        age = 8
        expected_res = 'ребенок'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_cannot_pass_str_as_age(self):
        age = 'old'
        with self.assertRaises(ValueError):
            get_social_status(age)

