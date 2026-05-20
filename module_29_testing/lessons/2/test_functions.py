import math
import pytest


def test_new_test():
    assert True


@pytest.mark.math
def test_math_sqrt():
    num = 25
    assert math.sqrt(num) == 5


def test_uppercase():
    assert "skillbox".upper() == "SKILLBOX"


def test_item_in_list():
    assert 777 in [item for item in [111, 222, 333, 777]]


@pytest.mark.math
def test_math_square():
    x = 5
    assert x * x == 25


@pytest.mark.math
def test_math_division():
    x = 5
    assert x // 2 == 2
