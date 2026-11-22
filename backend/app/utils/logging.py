import sys
import logging
from app.config import settings

class StructlogFallbackLogger:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def info(self, msg, **kwargs):
        extra = f" | {kwargs}" if kwargs else ""
        self._logger.info(f"{msg}{extra}")

    def warning(self, msg, **kwargs):
        extra = f" | {kwargs}" if kwargs else ""
        self._logger.warning(f"{msg}{extra}")

    def error(self, msg, **kwargs):
        extra = f" | {kwargs}" if kwargs else ""
        self._logger.error(f"{msg}{extra}")

    def critical(self, msg, **kwargs):
        extra = f" | {kwargs}" if kwargs else ""
        self._logger.critical(f"{msg}{extra}")

def get_logger(name: str = "newsletter"):
    try:
        import structlog
        return structlog.get_logger(name)
    except ImportError:
        base = logging.getLogger(name)
        return StructlogFallbackLogger(base)

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )
