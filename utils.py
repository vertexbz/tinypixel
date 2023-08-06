from typing import Union

from type import NeoColor


def to_hex_color(colors: Union[list[int], NeoColor]) -> str:
    if isinstance(colors, int):
        colors = [colors, colors, colors]
    else:
        colors = list(colors)

    if len(colors) == 3:
        colors = [*colors, 0]

    return ''.join('%02x' % color for color in colors)
