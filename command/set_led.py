from __future__ import annotations
from typing import Union
from command.base import Command
import re


class SetLedCommand(Command):
    def __init__(self, channel: int, index: int, r: int, g: int, b: int, w: int, send: bool):
        self.channel = channel
        self.index = index
        self.r = r
        self.g = g
        self.b = b
        self.w = w
        self.send = send

    @classmethod
    def from_line(cls, line: str) -> Union[None, Command]:
        match = re.match(
            r'^SET\s+CHANNEL=(\d+)\s+INDEX=(\d+)\s+R=(\d+)\s+G=(\d+)\s+B=(\d+)(?:\s+W=(\d+))?(?:\s+TRANSMIT=(\d))?$',
            line.upper()
        )

        if match:
            channel = int(match.group(1))
            index = int(match.group(2))
            r = int(match.group(3))
            g = int(match.group(4))
            b = int(match.group(5))
            w = -1 if len(match.group(6)) == 0 else int(match.group(6))
            send = match.group(7) != '0'

            if 0 <= channel <= 3 and index > 0 and 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and -1 <= w <= 255:
                return cls(channel, index, r, g, b, w, send)

        return None
