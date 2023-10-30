from __future__ import annotations
from . import cli
from .color import ColorParam
from interface import I2CInterface


@cli.command()
@cli.argument('channel', nargs=1, type=int)
@cli.option('--count', default=20, help='Number of LEDs.')
@cli.option('--mode', default='BGR', help='LEDs mode.')
def init(channel: int, count: int, mode: str):
    iface = I2CInterface(1)
    iface.init(channel, count, mode)
    iface.show(channel)
    iface.deinit()


@cli.command()
@cli.argument('channel', nargs=1, type=int)
def off(channel: int,):
    iface = I2CInterface(1)
    iface.off(channel)
    iface.deinit()


@cli.command()
@cli.argument('channel', nargs=1, type=int)
@cli.argument('color', nargs=1, type=ColorParam())
def fill(channel: int, color: tuple[int, int, int]):
    iface = I2CInterface(1)
    iface.fill(channel, color)
    iface.show(channel)
    iface.deinit()


@cli.command()
@cli.argument('channel', nargs=1, type=int)
@cli.argument('index', nargs=1, type=int)
@cli.argument('color', nargs=1, type=ColorParam())
def set(channel: int, index: int, color: tuple[int, int, int]):
    iface = I2CInterface(1)
    iface.set(channel, index, color)
    iface.show(channel)
    iface.deinit()


cli()
