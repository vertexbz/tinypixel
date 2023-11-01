from __future__ import annotations
from typing import Optional, Any, Type

FloatColor = tuple[float, float, float, float]
IntColor = tuple[int, int, int, int]


def _to_int(c: float):
    return int(c * 255. + .5)


def _to_float(c: int):
    return c / 255.


class ColorOrder(str):
    def __new__(cls, order: str):
        order = order.strip().upper()
        s = set(order)
        if 'R' in s and 'G' in s and 'B' in s and (len(s) == 3 or (len(s) == 4 and 'W' in s)):
            return super().__new__(cls, order)
        raise ValueError(f'"{order}" is not valid color order')


class Color:
    _int: Optional[IntColor] = None
    _float: Optional[FloatColor] = None

    @classmethod
    def from_float(cls, r: float, g: float, b: float, w: float = 0.) -> Color:
        c = Color()
        c._float = (r, g, b, w)
        return c

    @classmethod
    def from_int(cls, r: int, g: int, b: int, w: int = 0) -> Color:
        c = Color()
        c._int = (r, g, b, w)
        return c

    def float(self) -> FloatColor:
        if not self._float:
            self._float = (_to_float(self._int[0]), _to_float(self._int[1]), _to_float(self._int[2]), _to_float(self._int[3]))
        return self._float

    def int(self) -> IntColor:
        if not self._int:
            self._int = (_to_int(self._float[0]), _to_int(self._float[1]), _to_int(self._float[2]), _to_int(self._float[3]))
        return self._int

    def eq_float(self, other: FloatColor) -> bool:
        return self.float() == other

    def eq_int(self, other: IntColor) -> bool:
        return self.int() == other

    def eq_color(self, other: Color) -> bool:
        return self.int() == other.int()

    def __ne__(self, other: Any):
        return not self == other

    def __eq__(self, other: Any):
        if isinstance(other, Color):
            return self.eq_color(other)

        if isinstance(other, tuple) and len(other) == 4:
            if all(isinstance(o, float) for o in other):
                return self.eq_float(other)

            if all(isinstance(o, int) for o in other):
                return self.eq_int(other)

        return False


if __name__ == '__main__':
    assert Color.from_float(1, 1, 1, 1).float() == (1.0, 1.0, 1.0, 1.0)
    assert Color.from_int(255, 255, 255, 255).int() == (255, 255, 255, 255)
    assert Color.from_int(255, 255, 255, 255).float() == (1.0, 1.0, 1.0, 1.0)
    assert Color.from_float(1.0, 1.0, 1.0, 1.0).int() == (255, 255, 255, 255)

    assert Color.from_float(1, 1, 1, 1) == (1.0, 1.0, 1.0, 1.0)
    assert Color.from_int(255, 255, 255, 255) == (255, 255, 255, 255)
    assert Color.from_int(255, 255, 255, 255) == (1.0, 1.0, 1.0, 1.0)
    assert Color.from_float(1.0, 1.0, 1.0, 1.0) == (255, 255, 255, 255)
