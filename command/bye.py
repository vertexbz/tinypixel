from __future__ import annotations
from typing import Union
from command.base import Command


class ByeCommand(Command):
    @classmethod
    def from_line(cls, line: str) -> Union[None, Command]:
        if line.lower() == 'bye':
            return cls()

        return None
