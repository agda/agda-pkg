'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

from pathlib    import Path
from pony.orm   import *

from ..config   import ( AGDA_DEFAULTS_PATH
                       , AGDA_DIR_PATH
                       , AGDA_LIBRARIES_PATH
                       , AGDA_PKG_PATH
                       , AGDA_VERSION
                       , DATABASE_FILE_NAME
                       , DATABASE_FILE_PATH
                       , DATABASE_SEARCH_INDEXES_PATH
                       , GITHUB_USER
                       , INDEX_REPOSITORY_BRANCH
                       , INDEX_REPOSITORY_NAME
                       , INDEX_REPOSITORY_PATH
                       , INDEX_REPOSITORY_URL
                       , REPO
                       )

from ..service.readLibFile        import readLibFile
from ..service.writeAgdaDirFiles  import writeAgdaDirFiles
from ..service.database           import db, pw
from ..service.database           import ( Library
                                         , LibraryVersion
                                         , Keyword
                                         , TestedWith
                                         , Dependency
                                         )

import logging
import click_log as clog

# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def uninstall():
  pass

@db_session
def uninstallLibrary(libname, database=False, remove_cache=False):
  library = Library.get(name = libname)
  logger.info("Uninstalling")
  if library is None or not library.installed and not(remove_cache): 
    logger.info("  Library not installed.")
    logger.info("Nothing to uninstall.")
    return 

  for version in library.versions:
    if version.installed:
      try:
        vname = version.name
        if database:
          version.uninstall(True)
          version.delete()
        else:
          version.uninstall(remove_cache)
        logger.info("  Version removed ({}).".format(vname))
      except Exception as e:
        logger.error(e)
  try:
    if database:
      library.delete()
    else:
      library.uninstall()
  except Exception as e:
    logger.error(e)

  commit()
  writeAgdaDirFiles()
  logger.info("Successfully uninstallation ({}).".format(libname))

# --

@uninstall.command()
@click.argument('libname')
@click.option('--database'
             , type=bool
             , default=False
             , is_flag=True 
             , help='Remove from the database the package')
@click.option('--remove-cache'
             , type=bool
             , default=False
             , is_flag=True 
             , help='Remove all the files.')
@clog.simple_verbosity_option(logger)
@click.confirmation_option(prompt='Proceed?')
@db_session
def uninstall(libname, database, remove_cache):
  """Uninstall a package."""

  uninstallLibrary(libname, database, remove_cache)
