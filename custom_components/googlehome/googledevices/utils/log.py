"""Initialize logging."""
import logging
from .const import NAME

LOG = logging.getLogger(NAME)


def error(message):
    """Error log."""
    LOG.error(message)


def info(message):
    """Info log."""
    LOG.info(message)


def debug(message):
    """Info log."""
    LOG.debug(message)
