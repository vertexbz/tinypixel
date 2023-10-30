from __future__ import annotations
from abc import abstractmethod


class Interface:
    @abstractmethod
    def init(self, channel: int, count: int, typ: str) -> bool:
        pass

    @abstractmethod
    def fill(self, channel: int, color: tuple[int, int, int]) -> bool:
        pass

    @abstractmethod
    def set(self, channel: int, index: int, color: tuple[int, int, int]) -> bool:
        pass

    @abstractmethod
    def show(self, channel: int) -> bool:
        pass

    @abstractmethod
    def off(self, channel: int) -> bool:
        pass

    @abstractmethod
    def deinit(self):
        pass
