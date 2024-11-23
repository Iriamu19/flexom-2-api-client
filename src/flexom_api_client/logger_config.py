import os
import sys

from loguru import logger

log_level = os.getenv("LOG_LEVEL", "DEBUG")

logger.remove()
logger.add(sys.stdout, level=log_level)
__all__ = ["logger"]
