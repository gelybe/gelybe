
from typing import Union, Callable
from operator import sub, mul, truediv, add, pow
import logging

utils_logger = logging.getLogger('Utils Logger')
utils_logger.setLevel(level='ERROR')


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow,  # Add support for ^ as exponentiation
    '**': pow,  # Also support ** for exponentiation
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type {value}")
        #print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        #print("wrong operator value", value)
        utils_logger.error(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
