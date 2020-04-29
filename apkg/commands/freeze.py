'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
import logging
import click_log

from pony.orm            import db_session, select

from ..service.database  import db
from ..service.database  import ( Library , LibraryVersion )
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def freeze(): pass

@freeze.command()
@clog.simple_verbosity_option(logger)
@db_session
def freeze():
  """List of installed packages."""

  for library in select(l for l in Library if l.installed):
    installedVersion = library.getInstalledVersion()
    if installedVersion is not None:
      click.echo(installedVersion.freezeName)
