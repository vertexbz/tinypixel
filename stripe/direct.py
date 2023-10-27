from __future__ import annotations
from types import TracebackType
from logger import logger
from typing import Optional, Union, Sequence, Type
from stripe.base import Base
from stripe.dummy import Dummy
from stripe.config import StripeConfig
from type import NeoPin, NeoColor, NeoOrder
from utils import to_hex_color

try:
    import board
    import neopixel
except NotImplementedError:
    pass


def _pin_to_board(pin: NeoPin):
    if pin == 10:
        return board.D10
    elif pin == 12:
        return board.D12
    elif pin == 18:
        return board.D18
    elif pin == 21:
        return board.D21

    raise ValueError('Invalid pin ' + pin)

def _read_pixel_order(order: NeoOrder):
    if order == "RGB":
        return neopixel.RGB
    elif order == "GRB":
        return neopixel.GRB
    elif order == "RGBW":
        return neopixel.RGBW
    elif order == "GRBW":
        return neopixel.GRBW

    raise ValueError('invalid order: ' + order)


class Stripe(Base):
    def __init__(self, config: StripeConfig):
        self._logger = logger.getChild('stripe').getChild(f'channel {config.channel}')

        try:
            pin = _pin_to_board(config.pin)
            order = _read_pixel_order(config.order)

            self._logger.debug(f'pin {pin}, count: {config.count}')
            self._logger.debug(f'order {order}, bpp: {len(order)}')

            self.neopixel = neopixel.NeoPixel(
                pin,
                config.count,
                bpp=len(order),
                brightness=config.brightness,
                auto_write=False,
                pixel_order=_read_pixel_order(config.order)
            )
        except NameError:
            logger.getChild('stripe').warning(f'unknown board type, running in headless mode channel: {config.channel}')
            self.neopixel = Dummy(config)

    def deinit(self):
        self.neopixel.deinit()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.deinit()

    def fill(self, color: NeoColor, send: bool = True):
        self._logger.debug(f'filling with {to_hex_color(color)}')
        self.neopixel.fill(color)
        if send:
            self._logger.debug(f'rendering')
            self.neopixel.show()

    def set_pixel(self, index: Union[int, slice], color: Union[NeoColor, Sequence[NeoColor]], send: bool = True):
        self._logger.debug(f'setting pixel {index} to {to_hex_color(color)}')
        self.neopixel[index] = color
        if send:
            self._logger.debug(f'rendering')
            self.neopixel.show()

    def get_pixels(self, *indexes):
        if len(indexes) == 0:
            return self.neopixel[:]

    @property
    def brightness(self):
        return self.neopixel.brightness

    @brightness.setter
    def brightness(self, value: float):
        self.neopixel.brightness = value

    @property
    def chain_count(self):
        return self.neopixel.n
