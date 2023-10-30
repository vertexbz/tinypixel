from . import cli


@cli.command()
@cli.option('--count', default=1, help='Number of greetings.')
@cli.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        cli.echo(f"Hello {name}!")


cli()
