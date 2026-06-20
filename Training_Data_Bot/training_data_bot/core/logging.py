import logging
import sys
from contextlib import ContextDecorator

def get_logger(name: str) -> logging.Logger:
    """A diary writer for the factory"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class LogContext(ContextDecorator):
    """Context manager for detailed logging operations"""
    def __init__(self, operation_name: str, **kwargs):
        self.operation_name = operation_name
        self.kwargs = kwargs
        self.logger = get_logger("LogContext")

    def __enter__(self):
        self.logger.debug(f"Starting {self.operation_name} with args: {self.kwargs}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Error in {self.operation_name}: {exc_val}")
        else:
            self.logger.debug(f"Finished {self.operation_name}")
        return False