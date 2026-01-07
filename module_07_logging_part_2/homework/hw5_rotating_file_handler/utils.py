
from typing import Union, Callable
from operator import sub, mul, truediv, add
from logger_helper import get_logger
import logging
#from log_config import dict_config

#logging.config.dictConfig(dict_config)

utils_logger = get_logger('utils_logger')
#utils_logger.info('')

#utils_logger.error(f"wrong operator type 1")

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    #utils_logger = logging.getLogger('utils_logger')
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type {value}")
        #print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        #print("wrong operator value", value)
        print(utils_logger)
        utils_logger.info(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
