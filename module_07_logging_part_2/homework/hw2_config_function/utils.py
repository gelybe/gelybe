"""
Utils module
"""

from typing import Union, Callable
from operator import sub, mul, truediv, add, pow
import logging

utils_logger = logging.getLogger('Utils Logger')


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '**': pow,
    '^': pow,  # Support for both ** and ^ for exponentiation
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type {value}")
        raise ValueError("wrong operator type")

    # Convert ^ to ** for consistency
    operator = '**' if value == '^' else value

    if operator not in OPERATORS:
        utils_logger.error(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[operator]