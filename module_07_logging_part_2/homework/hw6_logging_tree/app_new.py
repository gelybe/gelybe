import sys
from utils import string_to_operator
from logger_helper import get_logger
from logging_tree import printout, format

# Инициализация логгеров
calculator_logger = get_logger('calculator_logger')
utils_logger = get_logger('utils_logger')

def calc(expression):
    """
    Вычисляет математическое выражение.
    Поддерживает два формата ввода:
    1. Строка с выражением (напр., '5**3')
    2. Список [число1, оператор, число2] (напр., [5, '**', 3])
    """
    calculator_logger.info(f'Expression: {expression}')
    
    try:
        # Пытаемся вычислить выражение напрямую, если это строка
        if isinstance(expression, str):
            try:
                result = eval(expression)
                calculator_logger.info(f"Result: {result}")
                calculator_logger.info(f"{expression} = {result}")
                return result
            except Exception as e:
                calculator_logger.error(f'Error evaluating expression: {e}')
                return None
            
        # Для обратной совместимости с вводом списком
        if not isinstance(expression, (list, tuple)) or len(expression) != 3:
            calculator_logger.error("Expected a list of 3 elements: [num1, operator, num2]")
            return None
            
        try:
            num_1 = float(expression[0])
            operator = str(expression[1])
            num_2 = float(expression[2])
        except (ValueError, TypeError) as e:
            calculator_logger.error(f'Error processing arguments: {e}')
            return None
        
        try:
            operator_func = string_to_operator(operator)
            result = operator_func(num_1, num_2)
            calculator_logger.info(f"Result: {result}")
            calculator_logger.info(f"{num_1} {operator} {num_2} = {result}")
            return result
        except Exception as e:
            calculator_logger.error(f'Error in calculation: {e}')
            return None
            
    except Exception as e:
        calculator_logger.error(f'Unexpected error: {e}')
        return None

if __name__ == '__main__':
    # Вывод дерева логгеров
    printout()
    with open('logging_tree.txt', 'w') as tree_file:
        tree_file.write(format.build_description())
    
    # Примеры использования
    calc('5**3')  # Строковое выражение
    calc([5, '**', 3])  # Список аргументов
