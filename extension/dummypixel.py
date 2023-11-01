from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from configfile import ConfigWrapper
    from gcode import GCodeDispatch
    from klippy import Printer
    from extras.led import PrinterLED

Color = tuple[float, float, float, float]


class Extension:
    name: str
    chain_count: int
    current_state: list[Color]

    def __init__(self, config: ConfigWrapper):
        gcode: GCodeDispatch = config.get_printer().lookup_object('gcode')

        # Config
        self.name = config.get_name().split()[-1]
        self.chain_count = config.getint('chain_count', minval=1)

        # Init fields
        self.current_state = [(0.0, 0.0, 0.0, 0.0)] * self.chain_count

        # Register handlers
        gcode.register_mux_command("SET_LED", "LED", self.name, self.cmd_SET_LED, desc=self.cmd_SET_LED_help)


    def get_led_count(self):
        return self.chain_count

    def get_status(self, *_):
        return {'color_data': self.current_state}

    def check_transmit(self, *_):
        pass

    def set_color(self, index: Optional[int], color: Color):
        if index is None:
            for i in range(self.chain_count):
                self.current_state[i] = color
        else:
            self.current_state[index - 1] = color

    cmd_SET_LED_help = "Set the color of an LED"

    def cmd_SET_LED(self, gcmd):
        red = gcmd.get_float('RED', 0., minval=0., maxval=1.)
        green = gcmd.get_float('GREEN', 0., minval=0., maxval=1.)
        blue = gcmd.get_float('BLUE', 0., minval=0., maxval=1.)
        white = gcmd.get_float('WHITE', 0., minval=0., maxval=1.)
        index = gcmd.get_int('INDEX', None, minval=1, maxval=self.chain_count)
        self.set_color(index, (red, green, blue, white))


def load_config_prefix(config: ConfigWrapper):
    extension = Extension(config)

    neo_key = f'neopixel {extension.name}'

    printer: Printer = config.get_printer()
    printer.objects[neo_key] = extension

    pled: PrinterLED = printer.load_object(config, 'led')
    pled.led_helpers[extension.name] = extension

    config.fileconfig.add_section(neo_key)

    config.fileconfig.set(neo_key, 'chain_count', extension.get_led_count())
    config.getsection(neo_key).getint('chain_count')

    return extension
