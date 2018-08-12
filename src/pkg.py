import click
from .commands.install import install
from .commands.info import info
from .commands.search import search


@click.group()
def cli():
    pass


cli.add_command(install)
cli.add_command(info)
cli.add_command(search)