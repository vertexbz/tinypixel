from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from confighelper import ConfigHelper
    from configfile import ConfigWrapper, PrinterConfig
    from klippy import Printer
    from extras.led import PrinterLED


def load_component(config: ConfigHelper):
    from .moonraker import Extension
    return Extension(config)


def load_config_prefix(config: ConfigWrapper):
    from .klipper import Extension
    extension = Extension(config)

    neo_key = f'neopixel {extension.name}'

    printer: Printer = config.get_printer()
    printer.objects[neo_key] = extension

    pled: PrinterLED = printer.load_object(config, 'led')
    pled.led_helpers[extension.name] = extension

    pconfig: PrinterConfig = printer.load_object(config, 'configfile')
    pconfig.status_settings[neo_key] = {
        'chain_count': extension.get_led_count()
    }

    return extension
