"""Provide log for other modules"""

from logentries import LogentriesHandler
import logging

__all__ = ['logger']

logger = logging.getLogger('rollbar')
logger.setLevel(logging.INFO)
LOGENTRIES_TOKEN = '01be0eb7-77c7-4c56-a1e3-1f87378271f1'
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)

logger.addHandler(logentries_handler)
