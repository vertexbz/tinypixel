from __future__ import annotations
from .utils import checksum
from .bus import Bus, Command

try:
    import logger
    logger = logger.named_logger(__name__)
except:
    import logging
    logger = logging.getLogger().getChild(__name__)


class Dummy(Bus):
    _buses_refs: dict[int, int] = {}

    def __init__(self, id: int):
        self._id = id
        self._logger = logger.getChild(str(id))

        if id not in Dummy._buses_refs:
            self._logger.debug(f'initializing smbus {id}')
            Dummy._buses_refs[id] = 0

        Dummy._buses_refs[id] += 1

    def send(self, command: Command, channel: int, *data: int) -> bool:
        cmd = (command.value << 4) | channel
        to_send = [*data, checksum(cmd, data or [0xFF])]
        self._logger.debug(f'writing i2c data: 69 {cmd:02X} ' + ' '.join(f'{b:02X}' for b in to_send))
        return True

    def deinit(self):
        Dummy._buses_refs[self._id] -= 1
        if Dummy._buses_refs[self._id] <= 0:
            self._logger.debug(f'closing smbus {self._id}')
