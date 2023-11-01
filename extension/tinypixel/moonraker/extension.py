from __future__ import annotations
from typing import Dict, Any, Optional
import logging

from common import WebRequest
from confighelper import ConfigError, ConfigHelper
from server import Server, ServerError
from .instance import Instance


def booleanize(s: Any) -> Optional[bool]:
    if isinstance(s, bool):
        return s
    elif isinstance(s, int):
        return s > 0
    elif isinstance(s, str) and len(s) > 0:
        s = s.strip().upper()
        if s not in ('ON', 'OFF', 'YES', 'NO', 'TRUE', 'FALSE'):
            raise ServerError(f'Unknown value \'{s}\'')
        return s in ('ON', 'YES', 'TRUE')
    return None


class Extension:
    _server: Server
    _instances: dict[str, Instance]

    def __init__(self, config: ConfigHelper) -> None:
        self._server = config.get_server()

        prefix_sections = config.get_prefix_sections("tinypixel")
        logging.info(f"tinypixel component loading instances: {prefix_sections}")
        self._instances = {}
        for section in prefix_sections:
            cfg = config[section]

            try:
                name_parts = cfg.get_name().split(maxsplit=1)
                if len(name_parts) != 2:
                    raise ConfigError(f"Invalid Section Name: {cfg.get_name()}")
                name: str = name_parts[1]

                logging.info(f"initializing tinypixel instance {name}")
                self._instances[name] = Instance(name, cfg)

            except Exception as e:
                # Ensures errors such as "Color not supported" are visible
                msg = f"Failed to initialise instance [{cfg.get_name()}]\n{e}"
                self._server.add_warning(msg)
                continue


        # Register two remote methods for GCODE
        self._server.register_remote_method("set_tinypixel_state", self.set_tinypixel_state)
        self._server.register_remote_method("set_tinypixel", self.set_tinypixel)

        # As moonraker is about making things a web api, let's try it
        # Yes, this is largely a cut-n-paste from power.py
        self._server.register_endpoint("/machine/tinypixel/strips", ["GET"], self._handle_list)
        self._server.register_endpoint("/machine/tinypixel/status", ["GET"], self._handle_batch_tinypixel_request)
        self._server.register_endpoint("/machine/tinypixel/on", ["POST"], self._handle_batch_tinypixel_request)
        self._server.register_endpoint("/machine/tinypixel/off", ["POST"], self._handle_batch_tinypixel_request)
        self._server.register_endpoint("/machine/tinypixel/strip", ["GET", "POST"], self._handle_single_tinypixel_request)

    async def component_init(self) -> None:
        try:
            for instance in self._instances.values():
                await instance.initialize()
        except Exception as e:
            logging.exception(e)

    async def set_tinypixel_state(self, name: str, s: Optional[str], preset: Optional[int] = -1) -> None:
        if name not in self._instances:
            raise ServerError(f'Unknown instance \'{name}\'')

        state = booleanize(s)

        if preset is not None and preset <= 0:
            preset = None

        await self._set_tinypixel_state(self._instances[name], state, preset)

    async def set_tinypixel(self, name: str, red: float = 0., green: float = 0., blue: float = 0., white: float = 0., index: Optional[int] = None, t: int = 1) -> None:
        if name not in self._instances:
            raise ServerError(f'Unknown instance \'{name}\'')

        transmit = booleanize(t) or False

        if red < 0:
            red = 0.0
        elif red > 1:
            red = 1.0

        if green < 0:
            green = 0.0
        elif green > 1:
            green = 1

        if blue < 0:
            blue = 0.0
        elif blue > 1:
            blue = 1.0

        if white < 0:
            white = 0.0
        elif white > 1:
            white = 1.0

        await self._set_tinypixel(self._instances[name], red, green, blue, white, index, transmit)

    async def _handle_single_tinypixel_request(self, web_request: WebRequest) -> Dict[str, Any]:
        name: str = web_request.get_str('name')
        if name not in self._instances:
            raise ServerError(f'Unknown instance \'{name}\'')

        preset: Optional[int] = web_request.get_int('preset', None)
        if preset is not None and preset <= 0:
            preset = None

        action = 'status'
        if web_request.get_action() == "POST":
            action = web_request.get_str('action').lower()
            if action not in ["on", "off", "toggle", "status"]:
                raise ServerError(f"Invalid requested action '{action}'")

        return await self._process_request(self._instances[name], action, preset)

    async def _handle_batch_tinypixel_request(self, web_request: WebRequest) -> Dict[str, Any]:
        args = web_request.get_args()
        ep = web_request.get_endpoint()
        if not args:
            raise ServerError("No arguments provided")

        result = {}
        command = ep.split("/")[-1]
        for name in args:
            if name in self._instances:
                result[name] = await self._process_request(self._instances[name], command, -1)
            else:
                result[name] = {"error": "instance_not_found"}
        return result

    def close(self) -> None:
        for instance in self._instances.values():
            instance.close()

    async def _handle_list(self, _: WebRequest) -> Dict[str, Any]:
        return {
            "instances": {
                name: instance.info()
                for name, instance in self._instances.items()
            }
        }

    async def _process_request(self, instance: Instance, command: str, preset: int) -> Dict[str, Any]:
        if command == "status":
            return instance.info()
        if command == "toggle":
            command = "off" if instance.is_on() else "on"
        if command in ["on", "off"]:
            await self._set_tinypixel_state(instance, command == "on", preset)
            return instance.info()

        raise ServerError(f"Unsupported tinypixel request: {command}")

    async def _set_tinypixel_state(self, instance: Instance, state: Optional[bool], preset: Optional[int] = None) -> None:
        if state is True:
            if preset is not None:
                instance.preset(preset)
            else:
                instance.on()
        elif state is False:
            instance.off()
        elif preset is not None:
            instance.preset(preset)

    async def _set_tinypixel(self, instance: Instance, red: float = 0., green: float = 0., blue: float = 0., white: float = 0., index: Optional[int] = None, transmit: bool = False) -> None:
        if index is None:
            instance.fill((red, green, blue, white))
        else:
            instance.set(index, (red, green, blue, white))
        if transmit:
            instance.show()
