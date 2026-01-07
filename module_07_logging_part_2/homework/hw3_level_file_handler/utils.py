
from typing import Union, Callable
from operator import sub, mul, truediv, add, pow
from logger_helper import get_logger

utils_logger = get_logger('Utils Logger')

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '**': pow,
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
