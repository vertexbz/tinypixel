from __future__ import annotations
import logging


class BufferingHandler(logging.Handler):
    def __init__(self, handler: logging.Handler):
        super().__init__()
        self.buffer: list[logging.LogRecord] = []
        self.handler = handler
        self.level = logging.NOTSET

    def get_name(self):
        return f'Buffered({self.handler.get_name()}'

    def set_name(self, name):
        self.handler.set_name(name)

    def _flush(self):
        logs = self.buffer
        self.buffer = []

        for record in logs:
            if record.levelno >= self.level:
                self.handler.handle(record)


    def setLevel(self, level):
        self.handler.setLevel(level)
        self.level = level
        self._flush()

    def format(self, record):
        return self.handler.format(record)

    def handle(self, record):
        if self.level == logging.NOTSET:
            self.buffer.append(record)
            return True

        return self.handler.handle(record)

    def flush(self):
        self.handler.flush()

    def close(self):
        self.handler.close()

    def handleError(self, record):
        self.handler.handleError(record)
