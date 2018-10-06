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
from ..service.logging            import logger, clog


# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def uninstall():
  pass

@db_session
def uninstallLibrary(libname, database=False, remove_cache=False):
  library = Library.get(name = libname)
  logger.info("Uninstalling")

  if library is None \
    or (not library.installed and not (remove_cache)): 

    logger.info("  Library not installed.")
    logger.info("Nothing to uninstall.")
    return


  try:
    if database:
      library.delete()
    else:
      if library.installed:
        library.uninstall(remove_cache)
        logger.info("Successfully uninstallation ({}).".format(libname))

    commit()
    writeAgdaDirFiles()
    return
  except Exception as e:
    logger.error(e)
    logger.error(" Unsuccessfully uninstallation.")

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
