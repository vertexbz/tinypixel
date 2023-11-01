from __future__ import annotations
from typing import Coroutine, Dict, Any, Callable, Union
import logging
from confighelper import ConfigError, ConfigHelper
from components.klippy_apis import KlippyAPI as APIComp
from server import Server, ServerError
from ..interface import Interface, I2CInterface
from ..types import Color, FloatColor, ColorOrder


class Instance:
    _server: Server
    name: str

    _bus: int
    _channel: int
    _chain_count: int
    _color_order: str
    _interface: Interface

    current_state: list[FloatColor]
    pending_state: dict[int, Color]
    _preset = None

    def __init__(self, name: str, cfg: ConfigHelper):
        self._server = cfg.get_server()
        self.name = name

        bus = cfg.getint("bus", 1)
        self._channel = cfg.getint("channel")
        self._chain_count: int = cfg.getint("chain_count", 1)
        try:
            self._color_order = ColorOrder(cfg.get('color_order', 'BGR'))
        except ValueError as e:
            raise ConfigError(str(e))

        # Init fields
        self.pending_state = {}
        self.current_state = [(0.0, 0.0, 0.0, 0.0)] * self._chain_count

        self._interface = I2CInterface(bus)
        self._server.register_event_handler('server:klippy_ready', self._init)

    def close(self):
        self._interface.deinit()

    async def _subscribe(self, object_type: str, callback: Callable[[dict], Union[None, Coroutine[Any, Any, None]]]) -> bool:
        try:
            kapis: APIComp = self._server.lookup_component('klippy_apis')
            await kapis.subscribe_objects({object_type: None})
        except ServerError as e:
            logging.info(f"{e}\nUnable to subscribe to {object_type} object")
            return False
        else:
            def updater(data: Dict[str, Any]):
                name = f"dummypixel {self.name}"
                if name in data:
                    callback(data[name])

            self._server.register_event_handler("server:status_update", updater)
            logging.info(f"{object_type} Subscribed")
            return True

    async def _init(self) -> None:
        await self._subscribe(f'dummypixel {self.name}', self._status_update)

    async def initialize(self) -> None:
        self._interface.init(self._channel, self._chain_count, self._color_order)
        self._interface.off(self._channel)

    # TODO
    async def _status_update(self, data: Dict[str, Any]) -> None:
        if "color_data" in data:
            index = 0
            for chain in data["color_data"]:
                red = chain.get("R", 0)
                green = chain.get("G", 0)
                blue = chain.get("B", 0)
                white = chain.get("W", 0)
                self._interface.set(self._channel, index, Color.from_float(red, green, blue, white).int())
                index += 1

        self._interface.show(self._channel)
        # todo transmit?

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "on": self.is_on(),
            "chain_count": self._chain_count,
            "preset": self._preset
        }

    def on(self):
        pass

    def off(self):
        pass

    def preset(self, preset):
        pass

    def is_on(self) -> bool:
        return False

    def fill(self, color: FloatColor):  # needs show
        pass

    def set(self, index: int, color: FloatColor):  # needs show
        pass

    def show(self):
        pass

