import logging


logger = logging.getLogger("uvicorn")


def get_logger() -> logging.Logger:
    """
    Returns a logger object
    """
    return logger
