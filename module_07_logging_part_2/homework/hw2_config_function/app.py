import sys
from utils import string_to_operator
import logging

#calculator_logger = logging.getLogger('Calculator Logger')
custom_handler = logging.StreamHandler(stream=sys.stdout)
#calculator_logger.addHandler(custom_handler)

logging.basicConfig(handlers=[custom_handler], level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
calculator_logger = logging.getLogger('Calculator Logger')

def calc(expression):
    calculator_logger.info(f'Arguments: {expression}')
    
    # Handle exponentiation first as it has higher precedence
    if '**' in expression:
        num_1, num_2 = expression.split('**', 1)
        operator = '**'
    elif '^' in expression:  # Also support ^ for exponentiation
        num_1, num_2 = expression.split('^', 1)
        operator = '^'
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
    calculator_logger.info(f"Result: {result} " )
    calculator_logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    # Test with different expressions
    test_expressions = ['2^3', '4**2', '2+3', '10/2', '5*4', '8-3']
    for expr in test_expressions:
        try:
            calc(expr)
        except Exception as e:
            calculator_logger.error(f"Error processing '{expr}': {e}")
    
    # Test with invalid input
    try:
        calc('2^a')
    except Exception as e:
        calculator_logger.error(f"Error processing '2^a': {e}")