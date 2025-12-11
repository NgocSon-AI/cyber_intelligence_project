import logging
import sys

class Logger:
    _instance = None

    @classmethod
    def get_logger(cls, name: str = "data-monitor"):
        """
        Get a logger instance with a consistent format across the project.
        Ensures handler is only added once.
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(name)
        return cls._instance

    @classmethod
    def _create_logger(cls, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Prevent adding duplicate handlers when calling get_logger() many times
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.propagate = False
        return logger


def get_logger(name="data-monitor"):
    return Logger.get_logger(name)
