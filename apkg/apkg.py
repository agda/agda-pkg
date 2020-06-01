'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click

from .commands                 import *
from .commands.clean           import clean
from .commands.create          import create
from .commands.freeze          import freeze
from .commands.list            import list
from .commands.info            import info
from .commands.init            import init
from .commands.install         import install
from .commands.nixos           import nixos
from .commands.uninstall       import uninstall
from .commands.search          import search
from .commands.update          import update
from .commands.upgrade         import upgrade
from .commands.environment     import environment
from .commands.write_defaults  import write_defaults

# ----------------------------------------------------------------------------

@click.group()
@click.version_option()
def cli():
  """A package manager for Agda."""

cli.add_command(init)
cli.add_command(nixos)
cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(freeze)
cli.add_command(list)
cli.add_command(info)
cli.add_command(clean)
cli.add_command(create)
cli.add_command(search)
cli.add_command(update)
cli.add_command(upgrade)
cli.add_command(environment)
cli.add_command(write_defaults)
