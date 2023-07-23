from __future__ import annotations
from typing import Union
from command.base import Command

from command.set_led import SetLedCommand
from command.off import OffCommand
from command.bye import ByeCommand
from command.read import ReadCommand
from command.count import CountCommand


ALL_COMMANDS = (SetLedCommand, OffCommand, ByeCommand, ReadCommand, CountCommand)
AnyCommand = Union[SetLedCommand, OffCommand, ByeCommand, ReadCommand, CountCommand]


class UnknownCommandError(Exception):
    pass


class Controller:
    def handle(self, command: AnyCommand) -> Union[bool, tuple[str, bool], str]:
        pass


def from_line(line: str) -> AnyCommand:
    line = line.strip()
    for cls in ALL_COMMANDS:
        result = cls.from_line(line)
        if result is not None:
            return result

    raise UnknownCommandError('Unrecognized instruction: ' + line)


__all__ = ['from_line', 'AnyCommand', 'UnknownCommandError', 'Controller']
