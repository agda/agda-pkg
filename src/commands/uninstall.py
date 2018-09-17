'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------

import click
from pathlib import Path
from ..config import ( AGDA_DEFAULTS_PATH
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

from ..service.readLibFile import readLibFile
from ..service.writeAgdaDirFiles import writeAgdaDirFiles
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pony.orm import *
import shutil

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

@uninstall.command()
@click.argument('libname')
@click.option('--database'
             , type=bool
             , default=False
             , help='remove from the database as well')
@clog.simple_verbosity_option(logger)
@click.confirmation_option(prompt='Are you sure you want to uninstall it?')
@db_session
def uninstall(libname, database):
  library = Library.get(name = libname)
  if library is None: return 
  for version in library.versions:
    try:
      if database:
        LibraryVersion.remove(version)
      version.uninstall()
    except Exception as e:
      logger.error(e)
      logger.error("u1")
      
  if database:
    Library.remove(library)
  else:
    library.uninstall()
  commit()
  writeAgdaDirFiles(True)
