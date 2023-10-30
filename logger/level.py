import logging

FATAL = logging.FATAL
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
INFO_LONG = logging.INFO - 1
DEBUG = logging.DEBUG
DEBUG_LONG = logging.DEBUG - 1

__all__ = [
    'FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
    'INFO_LONG', 'DEBUG_LONG'
]

