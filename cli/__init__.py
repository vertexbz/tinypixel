import click
import logger
__all__ = ['cli']


@click.group()
def cli():
    logger.info('Hostpixel')
    logger.set_level(logger.DEBUG_LONG)


cli.option = click.option
cli.echo = click.echo
cli.argument = click.argument
