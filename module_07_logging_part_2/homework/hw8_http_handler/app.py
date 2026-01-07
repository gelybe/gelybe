import sys
from utils import string_to_operator
from logger_helper import get_logger
from logging_tree import printout, format
import logging


def calc(expr):
    """
    Вычисляет выражение вида "число оператор число", например '5**3'
    Поддерживает: +, -, *, /, //, %, **.
    """
    calculator_logger.info(f'Arguments: {expr}')

    # Парсим строку вручную: ищем оператор с наибольшим приоритетом справа налево (для **)
    ops = ['**', '//', '%', '/', '*', '+', '-']
    a, op, b = None, None, None

    for operator in ops:
        if operator in expr:
            parts = expr.split(operator, 1)  # только первое вхождение
            if len(parts) == 2:
                a, b = parts[0].strip(), parts[1].strip()
                op = operator
                break

    if op is None:
        calculator_logger.error("Не удалось распознать оператор в выражении")
        return

    try:
        num_1 = float(a)
    except ValueError as e:
        calculator_logger.error(f'Error while converting number 1. Код ошибки - {e}')
        return

    try:
        num_2 = float(b)
    except ValueError as e:
        calculator_logger.error(f'Error while converting number 2. Код ошибки - {e}')
        return

    operator_func = string_to_operator(op)
    if not operator_func:
        calculator_logger.error(f"Оператор '{op}' не поддерживается")
        return

    try:
        result = operator_func(num_1, num_2)
        calculator_logger.info(f"Result: {result}")
        calculator_logger.info(f"{num_1} {op} {num_2} = {result}")
    except Exception as e:
        calculator_logger.error(f"Ошибка при вычислении: {e}")


if __name__ == '__main__':
    calculator_logger = get_logger('calculator_logger')
    utils_logger = get_logger('utils_logger')

    calculator_logger.info('Привет')
    utils_logger.info('hello')

    calc('5**3')
    calc('10/2')
    calc('7+3')