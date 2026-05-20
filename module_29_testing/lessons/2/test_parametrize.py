import pytest
import math


@pytest.mark.parametrize("degree, result", [(25, 5), (36, 6), (4, 2)])
def test_math_sqrt(degree, result):
    assert math.sqrt(degree) == result
