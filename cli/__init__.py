import click
__all__ = ['cli']


@click.group()
def cli():
    pass


cli.option = click.option
cli.echo = click.echo
