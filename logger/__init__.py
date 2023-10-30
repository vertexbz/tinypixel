from __future__ import annotations
import logging
import sys
from logger.filter_package_path import PackagePathFilter
from logger.formatter import CustomFormatter
from logger.format import FORMAT_DEBUG
from logger.buffered import BufferingHandler
from logger.level import *
import logger.level as level


Logger = logging.Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(logger))
stdout_handler.addFilter(PackagePathFilter())
buffered_stdout_handler = BufferingHandler(stdout_handler)
logger.addHandler(buffered_stdout_handler)
logger.debug('Stdout logger configured')


debug = logger.debug
info = logger.info
warn = logger.warn
warning = logger.warning
error = logger.error
critical = logger.critical
fatal = logger.fatal


def set_level(level):
    # logger.setLevel(level)
    buffered_stdout_handler.setLevel(level)


def named_logger(module: str):
    return logger.getChild(module)


def logToFile(logfile: str):
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(FORMAT_DEBUG))
    handler.addFilter(PackagePathFilter())
    logger.addHandler(handler)



__all__ = [
    'Logger', 'named_logger',
    'set_level', 'logToFile',
    'fatal', 'critical', 'error', 'warning', 'warn', 'info', 'debug',
    'FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
    'INFO_LONG', 'DEBUG_LONG', 'level'
]
