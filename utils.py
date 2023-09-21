import logging
from logging.handlers import RotatingFileHandler
from settings import Node


def get_logger(node: Node = Node.SERVER) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(f"{node.value}.log", maxBytes=2000000, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s::%(levelname)s::%(message)s"))

    logger.addHandler(file_handler)
    return logger
