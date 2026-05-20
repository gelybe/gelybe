import pytest


@pytest.fixture
def input_value() -> int:
    _input = 5
    return input


@pytest.mark.math
def test_math_square(input_value: int):
    x = input_value
    assert x * x == 25


@pytest.mark.math
def test_math_division(input_value: int):
    x = input_value
    assert x // 2 == 2
