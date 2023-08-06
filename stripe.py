from __future__ import annotations

from types import TracebackType
from logger import logger
from typing import Optional, Union, Sequence, Type
from type import NeoPin, NeoColor, NeoOrder
from adafruit_pixelbuf import PixelBuf

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

class StripeConfig:
    def __init__(self, channel: int, data):
        self.channel = channel
        self.pin = data.getint('pin')
        self.count = data.getint('count', 1)
        self.order = data['order']
        self.brightness = data.getfloat('brightness', 1.0)


class Dummy(PixelBuf):
    def __init__(self, config: StripeConfig):
        super().__init__(
            config.count, brightness=config.brightness, byteorder="RGBW", auto_write=False
        )
        self.n = config.count
        self.channel = config.channel

    def deinit(self):
        pass

    def show(self):
        logger.getChild('stripe').warning(f'rendering dummy channel {self.channel}')
        pass


class Stripe:
    def __init__(self, config: StripeConfig):
        try:
            order = _read_pixel_order(config.order)
            logger.getChild('stripe').warning(f'order {order}, bpp: {len(order)}')
            self.neopixel = neopixel.NeoPixel(
                _pin_to_board(config.pin),
                config.count,
                bpp=len(order),
                brightness=config.brightness,
                # auto_write=False,
                pixel_order=_read_pixel_order(config.order)
            )
        except NameError:
            logger.getChild('stripe').warning(f'unknown board type, running in headless mode channel: {config.channel}')
            self.neopixel = Dummy(config)


    def deinit(self):
        self.neopixel.deinit()
        pass

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
        self.neopixel.fill(color)
        if send:
            self.neopixel.show()

    def set_pixel(self, index: Union[int, slice], color: Union[NeoColor, Sequence[NeoColor]], send: bool = True):
        self.neopixel[index] = color
        if send:
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
