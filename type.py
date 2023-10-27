from __future__ import annotations
from typing import Union, Literal

NeoPin = Union[Literal[10], Literal[12], Literal[18], Literal[21]]
NeoOrder = Union[Literal['RGB'], Literal['GRB'], Literal['RGBW'], Literal['GRBW']]
NeoColor = Union[int, tuple[int, int, int], tuple[int, int, int, int]]
