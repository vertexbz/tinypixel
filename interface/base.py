from __future__ import annotations
from abc import abstractmethod
from enum import Enum


class Command(Enum):
    INIT = 0xF
    OFF = 0x0
    FILL = 0x1
    SET = 0x2
    SHOW = 0xE


class Interface:
    @abstractmethod
    def send(self, command: Command, channel: int, *data: int) -> bool:
        pass

    @abstractmethod
    def deinit(self):
        pass
