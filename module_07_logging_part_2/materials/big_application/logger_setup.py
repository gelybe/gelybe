import logging
import sys

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "screen": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "backupCount": 5,
            "formatter": "simple",
            "level": "ERROR",
            "filename": "skillbox.log"
        }
    },
    "loggers": {
        "skillbox": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
         }
    },
}
