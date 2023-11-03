from __future__ import annotations
from typing import Coroutine, Dict, Any, Callable, Union
import logging
from confighelper import ConfigError, ConfigHelper
from components.klippy_apis import KlippyAPI as APIComp
from server import Server, ServerError
from ..interface import I2CInterface
from ..stripe import Stripe, TransmissionError
from ..types import Color, ColorOrder


class Instance:
    _server: Server
    _stripe: Stripe
    name: str

    _brightness: float

    def __init__(self, name: str, cfg: ConfigHelper):
        self._server = cfg.get_server()
        self.name = name

        try:
            self._stripe = Stripe(
                I2CInterface(cfg.getint('bus'), cfg.getint('retries', 5, minval=1)),
                cfg.getint('channel'),
                cfg.getint('chain_count', minval=1),
                ColorOrder(cfg.get('color_order', 'BGR'))
            )
        except ValueError as e:
            raise ConfigError(str(e))

        self._brightness = cfg.getfloat('brightness', 1.0, minval=0.0, maxval=1.0)
        self._server.register_event_handler('server:klippy_ready', self._init)

    def close(self):
        self._stripe.deinit()

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

    async def _status_update(self, data: Dict[str, Any]) -> None:
        if "color_data" in data:
            index = 0
            for chain in data["color_data"]:
                red = chain.get("R", 0)
                green = chain.get("G", 0)
                blue = chain.get("B", 0)
                white = chain.get("W", 0)
                self._stripe[index] = Color.from_float(red, green, blue, white)
                index += 1

        self.show()

    async def initialize(self) -> None:
        try:
            self._stripe.init()
        except TransmissionError as e:
            raise ServerError(str(e))

    def on(self):
        self._stripe[None] = Color.from_float(self._brightness, self._brightness, self._brightness, self._brightness)

    def fill(self, color: Color):  # needs show
        self._stripe[None] = color

    def set(self, index: int, color: Color):  # needs show
        self._stripe[index] = color

    def off(self):
        self._stripe.off()

    def show(self):
        try:
            self._stripe.show()
        except TransmissionError as e:
            raise ServerError(str(e))

    def is_off(self) -> bool:
        return self._stripe.is_off()

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "off": self.is_off(),
            "chain_count": len(self._stripe),
            "color_data": self._stripe.state
        }



