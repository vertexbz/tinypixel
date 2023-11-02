from __future__ import annotations
from typing import Sequence, Union
from .interface import Interface
from .types import Color, IntColor, FloatColor, ColorOrder


class TransmissionError(Exception):
    def __init__(self, *args):
        msg = 'failed transmitting the command'
        if len(args) > 0 and isinstance(args[0], str):
            msg = f'failed transmitting {args[0]} command'
            args = args[1:]
        super().__init__(msg, *args)


class Stripe:
    _interface: Interface
    _channel: int
    _length: int
    _color_order: ColorOrder

    _current_state: list[FloatColor]
    _pending_state: dict[int, Color]

    def __init__(self, interface: Interface, channel: int, length: int, color_order: ColorOrder):
        self._interface = interface
        self._length = length
        self._channel = channel
        self._color_order = color_order

        self._pending_state = {}
        self._current_state = [(0.0, 0.0, 0.0, 0.0)] * self._length

    def init(self):
        self._interface.init(self._channel, self._length, self._color_order)
        self._interface.off(self._channel)

    def deinit(self):
        self._interface.deinit()

    def __len__(self):
        return self._length

    def __setitem__(self, index: Union[None, int, slice], color: Union[Color, Sequence[Color]]):
        if index is None:
            for i in range(self._length):
                self[i] = color
            return

        if isinstance(index, slice):
            start, stop, step = index.indices(len(self._current_state))
            for val_i, i in enumerate(range(start, stop, step)):
                if isinstance(color, Color):
                    self[i] = color
                else:
                    self[i] = color[val_i]
            return

        if color.eq_float(self._current_state[index]):
            if index in self._pending_state:
                del self._pending_state[index]
        else:
            self._pending_state[index] = color

    @property
    def state(self) -> list[FloatColor]:
        return self._current_state

    def show(self, *_):
        if len(self._pending_state) == 0:
            self._show()
        else:
            self.transmit()

    def transmit(self):
        if len(self._pending_state) == self._length:
            values = list(self._pending_state.values())
            if all(i == values[0] for i in values):
                if sum(values[0].int()) == 0:
                    self.off()
                else:
                    self._fill(values[0].int())
                    self._show()
                    self._current_state = [values[0].float()] * self._length
                    self._pending_state = {}
                return

        for index, color in self._pending_state.items():
            if color.eq_float(self._current_state[index]):
                continue
            self._set(index, color.int())
            self._current_state[index] = color.float()

        self._show()
        self._pending_state = {}

    def off(self):
        self._off()
        self._pending_state = {}
        self._current_state = [(0.0, 0.0, 0.0, 0.0)] * self._length

# raising helpers
    def _off(self):
        if not self._interface.off(self._channel):
            raise TransmissionError('off')

    def _show(self):
        if not self._interface.show(self._channel):
            raise TransmissionError('show')

    def _fill(self, color: IntColor):
        if not self._interface.fill(self._channel, color):
            raise TransmissionError('fill')

    def _set(self, index: int, color: IntColor):
        if not self._interface.set(self._channel, index, color):
            raise TransmissionError('set')

    def is_off(self) -> bool:
        return all(0 == sum(c) for c in self._current_state)
