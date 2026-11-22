import logging
from app.utils.logging import StructlogFallbackLogger

def get_logger(name: str = "app"):
    return StructlogFallbackLogger(logging.getLogger(name))
