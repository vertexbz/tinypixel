from __future__ import annotations
import sys
import argparse
import configparser
from utils import to_hex_color
from typing import Optional as Opt
from logger import logger, stdout_handler, file_handler
from server import ControllerAwareServer
from stripe import stripe_from_config, StripeConfig
from channels import Channels
from command import AnyCommand, Controller as BaseController
from command.set_led import SetLedCommand
from command.off import OffCommand
from command.bye import ByeCommand
from command.read import ReadCommand
from command.count import CountCommand
from command.fill import FillCommand

ControllerConfig = tuple[Opt[StripeConfig], Opt[StripeConfig], Opt[StripeConfig], Opt[StripeConfig]]


class Controller(BaseController):
    def __init__(self, channels: ControllerConfig):
        self._channel = Channels([stripe_from_config(config) for config in channels])
        self.off()

    def handle(self, cmd: AnyCommand):
        if isinstance(cmd, SetLedCommand):
            self._channel[cmd.channel].set_pixel(cmd.index, (cmd.r, cmd.g, cmd.b, cmd.w), cmd.send)
            return 'OK!'
        if isinstance(cmd, FillCommand):
            self._channel[cmd.channel].fill((cmd.r, cmd.g, cmd.b, cmd.w), cmd.send)
            return 'OK!'
        if isinstance(cmd, OffCommand):
            self.off()
            return 'OK!'
        if isinstance(cmd, CountCommand):
            count = self._channel[cmd.channel].chain_count
            return f'OK! {count}'
        if isinstance(cmd, ReadCommand):
            get = self._channel[cmd.channel].get_pixels
            pixels = get(cmd.index) if cmd.index is not None else get()
            response = ','.join(to_hex_color(colors) for colors in pixels)
            return f'OK! {response}'
        if isinstance(cmd, ByeCommand):
            return 'BYE!', False

        return 'Unsupported command'

    def off(self):
        for stripe in self._channel:
            if stripe is not None:
                stripe.fill((0, 0, 0, 0))


def main(sock: str, config: ControllerConfig):
    ControllerAwareServer(sock, Controller(config)).start()


def load_config_file(path: str) -> ControllerConfig:
    config = configparser.ConfigParser()
    config.read(path)

    channels_config = (None, None, None, None)
    for section_name in config.sections():
        if section_name not in [f'channel {c}' for c in range(3)]:
            raise ValueError(f'invalid config section: {section_name}')

        channel = int(section_name[8:])

        l = list(channels_config)
        l[channel] = StripeConfig(channel, config[section_name])
        channels_config = tuple(l)

    return channels_config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Hostpixel - Host neopixel control"
    )
    parser.add_argument(
        "-s", "--sock", default='/tmp/hostpixel', metavar='<unixsocket>',
        help="Path to hostpixel's unix domain socket"
    )
    parser.add_argument(
        "-c", "--configfile", default=None, metavar='<configfile>',
        help="Path to hostpixels's configuration file"
    )
    parser.add_argument(
        "-l", "--logfile", default=None, metavar='<logfile>',
        help="Path to hostpixels's log file"
    )

    cmd_line_args = parser.parse_args()

    if cmd_line_args.logfile is not None:
        logger.addHandler(file_handler(cmd_line_args.logfile))
        logger.removeHandler(stdout_handler)

    if not cmd_line_args.configfile:
        logger.error('no configfile provided')
        sys.exit(1)

    config = load_config_file(cmd_line_args.configfile)

    main(cmd_line_args.sock, config)
