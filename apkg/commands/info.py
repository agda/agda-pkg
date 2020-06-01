'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
import logging

from pprint                 import pprint
from pony.orm               import db_session

from ..service.readLibFile  import readLibFile
from ..service.database     import db, pw
from ..service.database     import ( Library
                                   , LibraryVersion
                                   , Keyword
                                   , TestedWith
                                   , Dependency
                                   )
from ..service.logging      import logger, clog

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def info(): pass

@info.command()
@click.argument('libname')
@click.option('--version'
             , type=str
             , default=""
             , help='Specific the package version.')
@click.option('--field'
             , type=str
             , default=""
             , help='Show a specific field')
@clog.simple_verbosity_option(logger)
@db_session
def info(libname, version, field):
  """Show information about installed packages."""

  library = Library.get(name = libname)

  if library is None:
    logger.error(" The library is not visible for agda-pkg.")
    return

  libVersion = LibraryVersion.get(library = library, name = version)

  if libVersion is None:
    libVersion = library.getInstalledVersion()

  if libVersion is None:
    libVersion = library.getLatestVersion()

  if libVersion is None:
    logger.error("The version does not exist. Try $ apkg search " + libname)
    return

  info = libVersion.info
  if field != "" :
    if field in info.keys():
      click.echo(info[field])
      return
    else:
      logger.error(" the field ("+ field + ") does not exist.")
      return

  pprint(info, indent=2)

