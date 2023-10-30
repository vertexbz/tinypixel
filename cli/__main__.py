from __future__ import annotations
from . import cli
from .color import ColorParam
from helper.ws281x import order_to_byte
from interface import I2CInterface, Command


@cli.command()
@cli.argument('channel', nargs=1, type=int)
@cli.option('--count', default=20, help='Number of LEDs.')
@cli.option('--mode', default='BGR', help='LEDs mode.')
def init(channel: int, count: int, mode: str):
    iface = I2CInterface(1)
    iface.send(Command.INIT, channel, count, order_to_byte(mode))
    iface.send(Command.SHOW, channel)


@cli.command()
@cli.argument('channel', nargs=1, type=int)
def off(channel: int,):
    iface = I2CInterface(1)
    iface.send(Command.OFF, channel)


@cli.command()
@cli.argument('channel', nargs=1, type=int)
@cli.argument('color', nargs=1, type=ColorParam())
def fill(channel: int, color: tuple[int, int, int]):
    iface = I2CInterface(1)
    iface.send(Command.FILL, channel, *color)
    iface.send(Command.SHOW, channel)


cli()
