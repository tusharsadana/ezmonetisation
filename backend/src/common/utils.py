# stdlib
import logging
from abc import ABCMeta

# thirdparty
import psutil

logger = logging.getLogger(__name__)


class SingletonWithArgs(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonWithArgs, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class Singleton(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__()
        return cls._instances[cls]


class SingletonABC(Singleton, ABCMeta):
    """Singleton ABC for resolving metaclass conflict"""


def log_ram_usage():
    """Log RAM usage"""
    try:
        ram_info = psutil.virtual_memory()
        logger.info(f"Total: {ram_info.total / 1024 / 1024 / 1024:.2f} GB")
        logger.info(
            f"Available: {ram_info.available / 1024 / 1024 / 1024:.2f} GB"
        )
        logger.info(f"Used: {ram_info.used / 1024 / 1024 / 1024:.2f} GB")
        logger.info(f"Percentage usage: {ram_info.percent}%")
    except FileNotFoundError:
        logger.info("CPU info not available on this system")
