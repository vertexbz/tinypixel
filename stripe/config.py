from __future__ import annotations


class StripeConfig:
    def __init__(self, channel: int, data):
        self.channel = channel
        self.pin = data.getint('pin')
        self.count = data.getint('count', 1)
        self.order = data['order']
        self.brightness = data.getfloat('brightness', 1.0)
