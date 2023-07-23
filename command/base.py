from __future__ import annotations
from typing import Union


class Command:
    @classmethod
    def from_line(cls, line: str) -> Union[None, Command]:
        pass
