import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Очистка существующих хэндлеров (чтобы не дублировать)
    if logger.handlers:
        logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
