# from logger_helper import LevelFileHandler
import logging


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


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s \n"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base"
        },
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "debug_file": "calc_debug.log",
            "error_file": "error_file.log",
            "mode": "a"
        },

        "utils_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "utils.log",
            "when": "s",
            "interval": 3,
            "backupCount": 3

        },
    },
    "loggers": {
        "calculator_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            # "propagate": False,
        },
        "utils_logger": {
            "level": "INFO",
            "handlers": ["utils_handler", "console"]
        },
    },

    # "filters": {},
    # "root": {} # == "": {}
}