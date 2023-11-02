from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
import logging
from gcode import CommandError
from .interface import I2CInterface
from .stripe import Stripe, TransmissionError
from .types import Color, FloatColor, ColorOrder

if TYPE_CHECKING:
    from configfile import ConfigWrapper
    from gcode import GCodeDispatch, GCodeCommand
    from klippy import Printer


class Extension:
    _printer: Printer
    _stripe: Stripe
    name: str

    def __init__(self, config: ConfigWrapper):
        self._printer = config.get_printer()
        gcode: GCodeDispatch = self._printer.lookup_object('gcode')

        self.name = config.get_name().split()[-1]
        try:
            self._stripe = Stripe(
                I2CInterface(config.getint('bus')),
                config.getint('channel'),
                config.getint('chain_count', minval=1),
                ColorOrder(config.get('color_order', 'BGR'))
            )
        except ValueError as e:
            raise config.error(str(e))

        # Register handlers
        self._printer.register_event_handler("klippy:connect", self._connect)
        self._printer.register_event_handler("klippy:disconnect", self._disconnect)
        gcode.register_mux_command("SET_LED", "LED", self.name, self.cmd_SET_LED, desc=self.cmd_SET_LED_help)

    def _connect(self, *_):
        try:
            self._stripe.init()
        except TransmissionError as e:
            raise CommandError(str(e))

    def _disconnect(self, *_):
        # self._stripe.deinit()
        pass

    def get_led_count(self):
        return len(self._stripe)

    def get_status(self, *_):
        return {'color_data': self._stripe.state}

    def set_color(self, index: Optional[int], color: Union[FloatColor, Color]):
        if not isinstance(color, Color):
            color = Color.from_float(color[0], color[1], color[2], color[3])

        if index is None:
            self._stripe[None] = color
        else:
            self._stripe[index - 1] = color

    cmd_SET_LED_help = "Set the color of an LED"

    def cmd_SET_LED(self, gcmd: GCodeCommand):
        red = gcmd.get_float('RED', 0., minval=0., maxval=1.)
        green = gcmd.get_float('GREEN', 0., minval=0., maxval=1.)
        blue = gcmd.get_float('BLUE', 0., minval=0., maxval=1.)
        white = gcmd.get_float('WHITE', 0., minval=0., maxval=1.)

        index = gcmd.get_int('INDEX', None, minval=1, maxval=len(self._stripe))
        transmit = gcmd.get_int('TRANSMIT', 0) > 0

        self.set_color(index, Color.from_float(red, green, blue, white))
        if transmit:
            self.check_transmit()

    def check_transmit(self):
        try:
            self._stripe.show()
        except TransmissionError as e:
            logging.exception(f"led update transmission error: {e}")
            raise CommandError(str(e))
