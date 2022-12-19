from functools import lru_cache
import logging

import requests


def get_logger(name: str) -> logging.Logger:
    """Returns an instance of the logger."""
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '[{levelname:^7}] {name}:{lineno} ({asctime}) - {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{',
    ))
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


@lru_cache()
def make_session() -> requests.Session:
    """Returns an HTTP session instance."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    })
    return session
