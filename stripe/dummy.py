from __future__ import annotations
from logger import logger
from stripe.config import StripeConfig
from adafruit_pixelbuf import PixelBuf


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
