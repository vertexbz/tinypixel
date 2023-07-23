from __future__ import annotations
import re
from typing import Optional
from command.base import Command


class ReadCommand(Command):
    def __init__(self, channel: int, index: Optional[int]):
        self.channel = channel
        self.index = index

    @classmethod
    def from_line(cls, line: str) -> Optional[Command]:
        match = re.match(r'^READ\s+CHANNEL=(\d+)(?:\s+INDEX=(\d))?$', line.upper())

        if match:
            channel = int(match.group(1))
            index = None if match.group(2) is None else int(match.group(2))

            if 0 <= channel <= 3 and (index is None or index > 0):
                return cls(channel, index)

        return None
