from __future__ import annotations
from .bus import Bus, Command
from .utils import order_to_byte, fix_color
from ..base import Interface


class I2CInterface(Interface):
    _bus: Bus

    def __init__(self, id: int):
        try:
            from .native import Native
            self._bus = Native(id)
        except:
            from .dummy import Dummy
            self._bus = Dummy(id)

    def deinit(self):
        self._bus.deinit()

    def init(self, channel: int, count: int, order: str) -> bool:
        return self._bus.send(Command.INIT, channel, count, order_to_byte(order))

    def fill(self, channel: int, color: tuple[int, int, int]) -> bool:
        # todo fix color
        return self._bus.send(Command.FILL, channel, *fix_color(3)(color))

    def set(self, channel: int, index: int, color: tuple[int, int, int]) -> bool:
        # todo fix color
        return self._bus.send(Command.FILL, channel, index, *fix_color(3)(color))

    def show(self, channel: int) -> bool:
        return  self._bus.send(Command.SHOW, channel)

    def off(self, channel: int) -> bool:
        return  self._bus.send(Command.OFF, channel)
