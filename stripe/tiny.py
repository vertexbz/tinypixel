from __future__ import annotations
from time import sleep
from enum import Enum
from functools import reduce
from logger import logger
from typing import Optional, Union, Sequence
from stripe.base import Base
from stripe.config import StripeConfig
from type import NeoColor, NeoOrder
from utils import to_hex_color

try:
    import smbus
except ModuleNotFoundError:
    # import smbus2 as smbus
    pass


def order_to_byte(order: NeoOrder) -> int:
    if order == "RGB":
        return ((0 << 6) | (0 << 4) | (1 << 2) | (2))
    if order == "RBG":
        return ((0 << 6) | (0 << 4) | (2 << 2) | (1))
    if order == "GRB":
        return ((1 << 6) | (1 << 4) | (0 << 2) | (2))
    if order == "GBR":
        return ((2 << 6) | (2 << 4) | (0 << 2) | (1))
    if order == "BRG":
        return ((1 << 6) | (1 << 4) | (2 << 2) | (0))
    if order == "BGR":
        return ((2 << 6) | (2 << 4) | (1 << 2) | (0))

    if order == "WRGB":
        return ((0 << 6) | (1 << 4) | (2 << 2) | (3))
    if order == "WRBG":
        return ((0 << 6) | (1 << 4) | (3 << 2) | (2))
    if order == "WGRB":
        return ((0 << 6) | (2 << 4) | (1 << 2) | (3))
    if order == "WGBR":
        return ((0 << 6) | (3 << 4) | (1 << 2) | (2))
    if order == "WBRG":
        return ((0 << 6) | (2 << 4) | (3 << 2) | (1))
    if order == "WBGR":
        return ((0 << 6) | (3 << 4) | (2 << 2) | (1))

    if order == "RWGB":
        return ((1 << 6) | (0 << 4) | (2 << 2) | (3))
    if order == "RWBG":
        return ((1 << 6) | (0 << 4) | (3 << 2) | (2))
    if order == "RGWB":
        return ((2 << 6) | (0 << 4) | (1 << 2) | (3))
    if order == "RGBW":
        return ((3 << 6) | (0 << 4) | (1 << 2) | (2))
    if order == "RBWG":
        return ((2 << 6) | (0 << 4) | (3 << 2) | (1))
    if order == "RBGW":
        return ((3 << 6) | (0 << 4) | (2 << 2) | (1))

    if order == "GWRB":
        return ((1 << 6) | (2 << 4) | (0 << 2) | (3))
    if order == "GWBR":
        return ((1 << 6) | (3 << 4) | (0 << 2) | (2))
    if order == "GRWB":
        return ((2 << 6) | (1 << 4) | (0 << 2) | (3))
    if order == "GRBW":
        return ((3 << 6) | (1 << 4) | (0 << 2) | (2))
    if order == "GBWR":
        return ((2 << 6) | (3 << 4) | (0 << 2) | (1))
    if order == "GBRW":
        return ((3 << 6) | (2 << 4) | (0 << 2) | (1))

    if order == "BWRG":
        return ((1 << 6) | (2 << 4) | (3 << 2) | (0))
    if order == "BWGR":
        return ((1 << 6) | (3 << 4) | (2 << 2) | (0))
    if order == "BRWG":
        return ((2 << 6) | (1 << 4) | (3 << 2) | (0))
    if order == "BRGW":
        return ((3 << 6) | (1 << 4) | (2 << 2) | (0))
    if order == "BGWR":
        return ((2 << 6) | (3 << 4) | (1 << 2) | (0))
    if order == "BGRW":
        return ((3 << 6) | (2 << 4) | (1 << 2) | (0))

    raise ValueError('invalid order: ' + order)


class Command(Enum):
    INIT = 0xF
    OFF = 0x0
    FILL = 0x1
    SET = 0x2
    SHOW = 0xE


class Interface:
    _buses: dict[int, Optional[smbus.SMBus]] = {}
    _buses_refs: dict[int, int] = {}

    def __init__(self, id: int):
        self._id = id
        self._logger = logger.getChild('smbus').getChild(f'id {id}')

        if id not in Interface._buses:
            self._logger.debug(f'initializing smbus {id}')
            Interface._buses_refs[id] = 0
            try:
                Interface._buses[id] = smbus.SMBus(id)
            except:
                Interface._buses[id] = None
                self._logger.warning(f'unknown board type, running in headless mode bus: {id}')

        self._bus = Interface._buses[id]
        Interface._buses_refs[id] += 1

    def _checksum(self, cmd: int, data: list[int]):
        return reduce(lambda a, b: a ^ b, [cmd, *data])

    def _flush(self):
        for _ in range(6):
            self._bus.write_byte(0x69, 0xFF)
            sleep(1 / 1000)
            if self._bus.read_byte(0x69) == 0x00:
                sleep(1 / 1000)
                return
            else:
                sleep(1 / 1000)

        self._logger.warning('couldn\'t achieve clean state')

    def write(self, command: Command, channel: int, *data: int):
        cmd = (command.value << 4) | channel
        to_send = [*data, self._checksum(cmd, data or [0xFF])]

        self._logger.debug(f'writing i2c data: 69 {cmd:02X} ' + ' '.join(f'{b:02X}' for b in to_send))

        if self._bus is not None:
            self._flush()
            self._bus.write_i2c_block_data(0x69, cmd, to_send)

            sleep(10 / 1000)

            if self._bus.read_byte(0x69) != 0x42:
                self._logger.error(f'failed transmitting command {cmd:02X}')

    def deinit(self):
        Interface._buses_refs[self._id] -= 1
        if Interface._buses_refs[self._id] <= 0:
            self._logger.debug(f'closing smbus {self._id}')
            if Interface._buses[self._id] is not None:
                Interface._buses[self._id].close()
            del Interface._buses[self._id]


class Tiny(Base):

    _bus: Interface
    _brightness: float

    def __init__(self, config: StripeConfig):
        self._channel = config.channel
        self._brightness = config.brightness
        self._bytes = len(config.order)

        self._logger = logger.getChild('stripe').getChild(f'{self._channel}')

        self._logger.debug(f'bus {config.bus}, count: {config.count}')
        self._logger.debug(f'order {config.order}, bpp: {len(config.order)}')

        self._bus = Interface(config.bus)
        self._bus.write(Command.INIT, self._channel, config.count, order_to_byte(config.order))

        self._buf = [(0, 0, 0, 0) if len(config.order) == 4 else (0, 0, 0)] * config.count

    def _fix_color(self, color: NeoColor) -> NeoColor:
        if isinstance(color, int):
            color = (color, color, color)

        if len(color) == 3 and self._bytes == 4:
            return color[0], color[1], color[2], 0

        if len(color) == 4 and self._bytes == 3:
            return color[0], color[1], color[2]

        return color

    def _apply_brightness(self, color: NeoColor) -> NeoColor:
        b = self._brightness
        if len(color) == 3:
            return int(color[0] * b), int(color[1] * b), int(color[2] * b)

        return int(color[0] * b), int(color[1] * b), int(color[2] * b), int(color[3] * b)

    def fill(self, color: NeoColor, send: bool = True):
        self._logger.debug(f'filling with {to_hex_color(color)}')
        color = self._fix_color(color)

        self._bus.write(Command.FILL, self._channel, *self._apply_brightness(color))
        self._buf = [color] * len(self._buf)
        if send:
            self._logger.debug(f'rendering')
            self._bus.write(Command.SHOW, self._channel)

    def set_pixel(self, index: Union[int, slice], color: Union[NeoColor, Sequence[NeoColor]], send: bool = True):
        self._logger.debug(f'setting pixel {index} to {to_hex_color(color)}')
        color = self._fix_color(color)

        self._bus.write(Command.SET, self._channel, index, *self._apply_brightness(color))
        self._buf[index] = color
        if send:
            self._logger.debug(f'rendering')
            self._bus.write(Command.SHOW, self._channel)

    def get_pixels(self, *indexes):
        if len(indexes) == 0:
            return self._buf[:]

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        if value > 1:
            value = 1
        if value < 0:
            value = 0

        self._brightness = value

    @property
    def chain_count(self):
        return len(self._buf)

    def deinit(self):
        self._bus.deinit()
