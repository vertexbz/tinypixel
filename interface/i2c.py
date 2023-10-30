from __future__ import annotations
from functools import reduce
from time import sleep
from typing import Optional
import logger
from .base import Command, Interface

try:
    import smbus
except ModuleNotFoundError:
    import smbus2 as smbus


logger = logger.named_logger(__name__)


class I2CInterface(Interface):
    _buses: dict[int, Optional[smbus.SMBus]] = {}
    _buses_refs: dict[int, int] = {}

    def __init__(self, id: int):
        self._id = id
        self._logger = logger.getChild(f'id {id}')

        if id not in I2CInterface._buses:
            self._logger.debug(f'initializing smbus {id}')
            I2CInterface._buses_refs[id] = 0
            try:
                I2CInterface._buses[id] = smbus.SMBus(id)
            except:
                I2CInterface._buses[id] = None
                self._logger.warning(f'unknown board type, running in headless mode bus: {id}')

        self._bus = I2CInterface._buses[id]
        I2CInterface._buses_refs[id] += 1

    def _checksum(self, cmd: int, data: list[int]):
        return reduce(lambda a, b: a ^ b, [cmd, *data])

    def send(self, command: Command, channel: int, *data: int) -> bool:
        cmd = (command.value << 4) | channel
        to_send = [*data, self._checksum(cmd, data or [0xFF])]

        for _ in range(5):
            self._logger.debug(f'writing i2c data: 69 {cmd:02X} ' + ' '.join(f'{b:02X}' for b in to_send))
            if self._bus is None:
                return True

            self._bus.write_i2c_block_data(0x69, cmd, to_send)
            sleep(10 / 1000)
            if self._bus.read_byte(0x69) == 0x42:
                self._logger.debug('command transmitted successfully')
                return True
            else:
                self._logger.error(f'failed transmitting command {cmd:02X}')

        return False

    def deinit(self):
        I2CInterface._buses_refs[self._id] -= 1
        if I2CInterface._buses_refs[self._id] <= 0:
            self._logger.debug(f'closing smbus {self._id}')
            if I2CInterface._buses[self._id] is not None:
                I2CInterface._buses[self._id].close()
            del I2CInterface._buses[self._id]
