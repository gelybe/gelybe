import sys
from utils import string_to_operator
from logger_helper import get_logger

calculator_logger = get_logger('Calculator Logger')


def calc(expression):
    calculator_logger.info(f'Arguments: {expression}')
    
    # Handle exponentiation first as it has higher precedence
    if '**' in expression:
        num_1, num_2 = expression.split('**', 1)
        operator = '**'
    else:
        # For other operators, find the operator in the string
        for op in ['+', '-', '*', '/']:
            if op in expression:
                num_1, num_2 = expression.split(op, 1)
                operator = op
                break
        else:
            calculator_logger.error('No valid operator found')
            return

    try:
        num_1 = float(num_1)
    except ValueError as e:
        calculator_logger.error(f'Error while converting number 1. Код ошибки - {e}')

    try:
        num_2 = float(num_2)
    except ValueError as e:
        calculator_logger.error(f'Error while converting number 2. Код ошибки - {e}')

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)
    calculator_logger.info(f"Result: {result} ")
    calculator_logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    calc('5**3')