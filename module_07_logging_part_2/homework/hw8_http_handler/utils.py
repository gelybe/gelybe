from typing import Union, Callable
from operator import sub, mul, truediv, add, pow  # Добавлен pow
from logger_helper import get_logger
import logging

utils_logger = get_logger('utils_logger')

# Словарь операторов — добавлен '**' -> pow
OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '**': pow,  # Поддержка возведения в степень
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

    if value not in OPERATORS:
        utils_logger.error(f"wrong operator value {value}")  # Лучше использовать error
        raise ValueError("wrong operator value")

    return OPERATORS[value]
