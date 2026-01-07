import logging
import logging.config
import sys


# from log_config import dict_config

class LevelFileHandler(logging.Handler):
    def __init__(self, debug_file, error_file, mode='a'):
        super().__init__()
        self.debug_file = debug_file
        self.error_file = error_file
        self.mode = mode
        self.setFormatter(logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)s| %(message)s \n'))

    def emit(self, record):
        message = self.format(record)
        if record.levelname != 'ERROR':
            with open(self.debug_file, mode=self.mode) as debug_file:
                debug_file.write(message)
        elif record.levelname == 'ERROR':
            with open(self.error_file, mode=self.mode) as error_file:
                error_file.write(message)

        # return super().emit(record)

# def get_logger(name):
# custom_handler = LevelFileHandler(debug_file='calc_debug.log', error_file='calc_error.log')
# logging.basicConfig(handlers=[custom_handler], level='DEBUG')
# logging.config.dictConfig(dict_config)
#   logger = logging.getLogger(name)
#    return logger
