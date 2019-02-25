'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

from .commands            import *
from .commands.clean      import clean
from .commands.create     import create
from .commands.freeze     import freeze
from .commands.list       import list
from .commands.info       import info
from .commands.init       import init
from .commands.install    import install
from .commands.uninstall  import uninstall
from .commands.search     import search
from .commands.update     import update
from .commands.upgrade    import upgrade

# ----------------------------------------------------------------------------

@click.group()
@click.version_option()
def cli():
  """The Agda Package manager."""

cli.add_command(init)
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
