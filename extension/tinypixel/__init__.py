from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from confighelper import ConfigHelper
    from configfile import ConfigWrapper
    from klippy import Printer


def load_component(config: ConfigHelper):
    from .moonraker import Extension
    return Extension(config)


def load_config_prefix(config: ConfigWrapper):
    from .klipper import Extension
    extension = Extension(config)

    printer: Printer = config.get_printer()
    printer.objects[f'neopixel {extension.name}'] = extension
    return extension
