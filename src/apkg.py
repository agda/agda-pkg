'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click
from .commands import *

from .commands.clean    import clean
from .commands.download import download
from .commands.freeze   import freeze
from .commands.info     import info
from .commands.init     import init
from .commands.install    import install
from .commands.uninstall  import uninstall
from .commands.search   import search
from .commands.update   import update
from .commands.upgrade  import upgrade

from .service.database import db, pw
from .service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pprint   import pprint
from pony.orm import *

@click.group()
@click.version_option()
def cli():
  """Package manager for Agda v2.5.4+"""

cli.add_command(init)
cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(freeze)
cli.add_command(info)
cli.add_command(clean)
cli.add_command(search)
# cli.add_command(update)
# cli.add_command(download)
cli.add_command(upgrade)
