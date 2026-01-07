import sys
from utils import string_to_operator
from logger_helper import get_logger
#from log_config import dict_config
import logging
from logging_tree import printout, format

def calc(expression):
    calculator_logger.info(f'Expression: {expression}')
    
    try:
        # Пытаемся вычислить выражение напрямую, если это строка
        if isinstance(expression, str):
            result = eval(expression)
            calculator_logger.info(f"Result: {result}")
            calculator_logger.info(f"{expression} = {result}")
            return result
            
        # Для обратной совместимости с вводом списком
        if len(expression) != 3:
            raise ValueError("Ожидается 3 аргумента: число1 оператор число2")
            
        num_1 = float(expression[0])
        operator = expression[1]
        num_2 = float(expression[2])
        
        operator_func = string_to_operator(operator)
        result = operator_func(num_1, num_2)
        calculator_logger.info(f"Result: {result}")
        calculator_logger.info(f"{num_1} {operator} {num_2} = {result}")
        return result
        
    except (ValueError, TypeError) as e:
        calculator_logger.error(f'Ошибка при вычислении: {e}')
    except Exception as e:
        calculator_logger.error(f'Непредвиденная ошибка: {e}')
    return None

if __name__ == '__main__':
    calculator_logger = get_logger('calculator_logger')
    utils_logger = get_logger('utils_logger')
    
    utils_logger.info('hello')
    calculator_logger.info('Привет')
    
    # Примеры использования:
    calc('5**3')  # Строковое выражение
    calc([5, '**', 3])  # Старый формат