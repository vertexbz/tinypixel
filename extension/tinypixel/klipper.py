from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
import logging
from .interface import Interface, I2CInterface
from .types import Color, FloatColor

if TYPE_CHECKING:
    from configfile import ConfigWrapper
    from extras.led import PrinterLED
    from gcode import GCodeDispatch
    from klippy import Printer


class Extension:
    _printer: Printer
    _channel: int
    _chain_count: int
    _color_order: str
    _interface: Interface

    current_state: list[FloatColor]
    pending_state: dict[int, Color]

    def __init__(self, config: ConfigWrapper):
        self._printer = config.get_printer()
        gcode: GCodeDispatch = self._printer.lookup_object('gcode')
        pled: PrinterLED = self._printer.load_object(config, "led")

        # Config
        name = config.get_name().split()[-1]
        bus = config.getint('bus')
        self._channel = config.getint('channel')
        self._chain_count = config.getint('chain_count', minval=1)
        # TODO validate color order
        self._color_order = config.get('color_order', 'BGR').strip().upper()

        # Init fields
        self.pending_state = {}
        self.current_state = [(0.0, 0.0, 0.0, 0.0)] * self._chain_count

        # Init interface
        self._interface = I2CInterface(bus)

        # Register handlers
        self._printer.register_event_handler("klippy:connect", self._connect)
        gcode.register_mux_command("SET_LED", "LED", name, self.cmd_SET_LED, desc=self.cmd_SET_LED_help)
        pled.led_helpers[name] = self

    def _connect(self, *_):
        self._interface.init(self._channel, self._chain_count, self._color_order)
        self._interface.off(self._channel)

    def get_led_count(self):
        return self._chain_count

    def get_status(self, *_):
        return { 'color_data': self.current_state}

    def check_transmit(self, *_):
        if len(self.pending_state) == 0:
            return
        try:
            self._transmit()
        except self._printer.command_error:
            logging.exception("led update transmit error")

    def _set_color(self, index: int, color: Color):
        if color.eq_float(self.current_state[index]):
            del self.pending_state[index]
        else:
            self.pending_state[index] = color

    def set_color(self, index: Optional[int], color: Union[FloatColor, Color]):
        if not isinstance(color, Color):
            color = Color.from_float(color[0], color[1], color[2], color[3])

        if index is None:
            for i in range(self._chain_count):
                self._set_color(i, color)
        else:
            self._set_color(index, color)

    def _transmit(self):
        def inner():
            if len(self.pending_state) == self._chain_count:
                values = list(self.pending_state.values())
                if all(i == values[0] for i in values):
                    self._interface.fill(self._channel, values[0].int())
                    self.current_state = [values[0].float()] * self._chain_count
                    return

            for index, color in self.pending_state.items():
                self._interface.set(self._channel, index, color.int())
                self.current_state[index] = color.float()

        inner()
        self.pending_state = {}
        self._interface.show(self._channel)

    cmd_SET_LED_help = "Set the color of an LED"

    def cmd_SET_LED(self, gcmd):
        red = gcmd.get_float('RED', 0., minval=0., maxval=1.)
        green = gcmd.get_float('GREEN', 0., minval=0., maxval=1.)
        blue = gcmd.get_float('BLUE', 0., minval=0., maxval=1.)
        white = gcmd.get_float('WHITE', 0., minval=0., maxval=1.)

        index = gcmd.get_int('INDEX', None, minval=1, maxval=self._chain_count)
        transmit = gcmd.get_int('TRANSMIT', 1) > 0

        self.set_color(index, Color.from_float(red, green, blue, white))
        if transmit:
            self.check_transmit()
