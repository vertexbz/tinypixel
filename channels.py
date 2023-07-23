from typing import Optional
from stripe import Stripe


class Channels:
    def __init__(self, stripes: tuple[Optional[Stripe], Optional[Stripe], Optional[Stripe], Optional[Stripe]]):
        self._channel = stripes

    def __getitem__(self, item: int) -> Stripe:
        if not isinstance(item, int):
            raise KeyError('key has to be an integer')
        if 0 > item >= len(self._channel):
            raise KeyError('key has to be between 0 and 3')
        if self._channel[item] is None:
            raise KeyError(f'channel {item} is not defined')

        return self._channel[item]
