# TODO переписать реализацию ini-файла в формате dict-конфигурации.


import logging

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"
        },
        "console": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"

        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "console",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "logfile.log",
        },

    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["file", "console", ],
            "propagate": False,
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", ],
        }

    },

    # "filters": {},
    # "root": {} # == "": {}
}