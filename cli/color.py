from __future__ import annotations
from typing import Optional, Any
from gettext import gettext
import re
import click
import random

_rand_8bit_pool: dict[str, list[int]] = {}


def rand_8bit_init() -> list[int]:
    pool = set(range(10, 230 + 1))
    for banned in {52, 88, 124, 160, 196}:
        pool.remove(banned)

    pool = list(pool)
    random.Random(8).shuffle(pool)
    return pool


def rand_8bit(pool: str = ''):
    if pool not in _rand_8bit_pool or len(_rand_8bit_pool[pool]) == 0:
        _rand_8bit_pool[pool] = rand_8bit_init()
    return _rand_8bit_pool[pool].pop()


class ColorParam(click.types.StringParamType):
    match = re.compile(r'^[A-F0-9]{6}$')

    def convert(self, value: Any, param: Optional["Parameter"], ctx: Optional["Context"]) -> Any:
        converted: str = super().convert(value, param, ctx)
        if converted.startswith('#'):
            converted = converted[1:]
        converted = converted.upper()

        if self.match.match(converted):
            return int(converted[0:2], 16), int(converted[2:4], 16), int(converted[4:6], 16)

        self.fail(
            gettext("{value!r} is not correct hex color.").format(value=value),
            param,
            ctx,
        )

    def __repr__(self) -> str:
        return 'COLOR'
