import click

from .commands.download import download
from .commands.info import info
from .commands.install import install
from .commands.search import search
from .commands.update import update


@click.group()
def cli():
  pass

cli.add_command(install)
cli.add_command(info)
cli.add_command(search)
cli.add_command(update)
cli.add_command(download)