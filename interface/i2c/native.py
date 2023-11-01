from __future__ import annotations
from time import sleep
from typing import Optional
import smbus2 as smbus
from .bus import Bus, Command
from .utils import checksum

try:
    import logger
    logger = logger.named_logger(__name__)
except:
    import logging
    logger = logging.getLogger().getChild(__name__)


class Native(Bus):
    _buses: dict[int, Optional[smbus.SMBus]] = {}
    _buses_refs: dict[int, int] = {}

    def __init__(self, id: int):
        self._id = id
        self._logger = logger.getChild(str(id))

        if id not in Native._buses:
            try:
                sm_bus = smbus.SMBus(id)
            except FileNotFoundError as e:
                self._logger.warning(f'unknown board type, bus {id} running in headless mode')
                raise e

            self._logger.debug(f'initializing smbus {id}')
            Native._buses_refs[id] = 0
            Native._buses[id] = sm_bus

        self._bus = Native._buses[id]
        Native._buses_refs[id] += 1

    def send(self, command: Command, channel: int, *data: int) -> bool:
        cmd = (command.value << 4) | channel
        to_send = [*data, checksum(cmd, data or [0xFF])]

        for _ in range(5):
            self._logger.debug(f'writing i2c data: 69 {cmd:02X} ' + ' '.join(f'{b:02X}' for b in to_send))

            try:
                self._bus.write_i2c_block_data(0x69, cmd, to_send)
                sleep(5 / 1000)
                result = self._bus.read_byte(0x69)
                if result == 0x42:
                    self._logger.debug('command transmitted successfully')
                    return True
                else:
                    self._logger.error(f'failed transmitting command, result {result:02X}')
            except OSError as e:
                if e.errno == 121:
                    self._logger.error('failed transmitting command [OSError: 121]: Remote I/O error')
                elif e.errno == 5:
                    self._logger.error('failed transmitting command [OSError: 5]: I/O error')
                else:
                    raise e

            sleep(5 / 1000)

        return False

    def deinit(self):
        Native._buses_refs[self._id] -= 1
        if Native._buses_refs[self._id] <= 0:
            self._logger.debug(f'closing smbus {self._id}')
            if Native._buses[self._id] is not None:
                Native._buses[self._id].close()
            del Native._buses[self._id]
