'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------

import click

from pony.orm import db_session, select

from ..service.database import db
from ..service.database import ( Library , LibraryVersion )

import logging
import click_log as clog
# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def freeze():
    pass

@freeze.command()
@clog.simple_verbosity_option(logger)
@db_session
def freeze():
  """Output installed packages in requirements format.
     packages are listed in a case-insensitive sorted order.
  """

  libraries = select(l for l in Library if l.installed)[:]

  for library in libraries:
    versions = [v for v in library.versions if v.installed]

    if len(versions) != 1:
      logger.error("Database is corrupted. This can cause import problems in Agda.")
      logger.info("Repair the database by running: apkg init")
      return

    installedVersion = versions[0]
    click.echo(library.name + "==" + installedVersion.name)
