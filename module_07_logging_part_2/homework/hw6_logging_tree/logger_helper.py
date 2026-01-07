import logging
import logging.config
import sys
from log_config import dict_config


# from log_config import dict_config


# return super().emit(record)


def get_logger(name):
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(name)
    return logger
