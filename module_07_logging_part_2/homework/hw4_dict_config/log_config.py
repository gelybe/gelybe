from logger_helper import LevelFileHandler

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
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
        #"file_error": {
        #    "()": LevelFileHandler,
        #    "level": "ERROR",
        #    "formatter": "base",
        #    "filename": "error_file.log",
        #    "mode": "a"
        #}
    },
    "loggers": {
        "calculator_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            # "propagate": False,
        }
    },

    # "filters": {},
    # "root": {} # == "": {}
}