from typing import Optional
from stripe import Stripe


class InvalidChannelError(Exception):
    pass


class Channels:
    def __init__(self, stripes: tuple[Optional[Stripe], Optional[Stripe], Optional[Stripe], Optional[Stripe]]):
        self._channel = stripes

    def __iter__(self):
        return filter(lambda s: s is not None, self._channel)

    def __getitem__(self, item: int) -> Stripe:
        if not isinstance(item, int):
            raise InvalidChannelError('key has to be an integer')
        if 0 > item >= len(self._channel):
            raise InvalidChannelError('key has to be between 0 and 3')
        if self._channel[item] is None:
            raise InvalidChannelError(f'channel {item} is not defined')

        return self._channel[item]
