from __future__ import annotations
from typing import Union
from command.base import Command
import re


class FillCommand(Command):
    def __init__(self, channel: int, r: int, g: int, b: int, w: int, send: bool):
        self.channel = channel
        self.r = r
        self.g = g
        self.b = b
        self.w = w
        self.send = send

    @classmethod
    def from_line(cls, line: str) -> Union[None, Command]:
        match = re.match(
            r'^FILL\s+CHANNEL=(\d+)\s+R=(\d+)\s+G=(\d+)\s+B=(\d+)(?:\s+W=(\d+))?(?:\s+TRANSMIT=(\d))?$',
            line.upper()
        )

        if match:
            channel = int(match.group(1))
            r = int(match.group(2))
            g = int(match.group(3))
            b = int(match.group(4))
            w = -1 if match.group(5) is None else int(match.group(5))
            send = match.group(6) != '0'

            if 0 <= channel <= 3 and 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and -1 <= w <= 255:
                return cls(channel, r, g, b, w, send)

        return None
