from __future__ import annotations
import re
from typing import Optional
from command.base import Command


class CountCommand(Command):
    def __init__(self, channel: int):
        self.channel = channel

    @classmethod
    def from_line(cls, line: str) -> Optional[Command]:
        match = re.match(r'^COUNT\s+CHANNEL=(\d+)$', line.upper())

        if match:
            channel = int(match.group(1))

            if 0 <= channel <= 3:
                return cls(channel)

        return None
