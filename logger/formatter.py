from __future__ import annotations
import logging
from sty import fg, ef
from cli.color import rand_8bit
from logger.format import FORMAT_DEBUG, FORMAT_SHORT
import logger.level as level


class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: lambda f: f,
        logging.INFO: lambda f: f,
        logging.WARNING: lambda f: fg.yellow + f + fg.rs,
        logging.ERROR: lambda f: fg.red + f + fg.rs,
        logging.CRITICAL: lambda f: fg.li_red + f + fg.rs,
    }

    _colors = {'root': ''}

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger = logger

    def color_child(self, name: str):
        if name not in self._colors:
            self._colors[name] = fg(rand_8bit('logger.child'))

        return self._colors[name]

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        record.msg = log_fmt(record.msg)

        color = self.color_child(record.name)

        format = FORMAT_DEBUG if self.logger.level in (level.INFO_LONG, level.DEBUG_LONG) else FORMAT_SHORT
        format = format.replace(ef.rs, ef.rs + color)
        format = format.replace(fg.rs, fg.rs + color)

        formatter = logging.Formatter(color + format + fg.rs)
        return formatter.format(record)
