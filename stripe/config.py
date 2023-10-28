from __future__ import annotations

from configparser import SectionProxy


class StripeConfig:
    def __init__(self, channel: int, data: SectionProxy):
        self.channel = channel
        self.pin = data.getint('pin', fallback=-1)
        self.bus = data.getint('bus', fallback=-1)
        self.count = data.getint('count', 1)
        self.order = data['order']
        self.brightness = data.getfloat('brightness', 1.0)
