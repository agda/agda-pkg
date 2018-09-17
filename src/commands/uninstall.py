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
@click.option('--remove-files'
             , type=bool
             , default=False
             , help='remove all source code related')
@clog.simple_verbosity_option(logger)
@db_session
def uninstall(libname, remove_files):
  library = Library.get(name = libname, installed = True)
  if library is not None:
    if click.confirm("Uninstalling... " + libname):
      try:
        library.installed = False
        library.default   = False
        for v in library.versions:
          v.installed = False
          if v.user_version:
            try:
              msg = "Delete all files in " + v.installationPath
              if remove_files or click.confirm(msg):
                shutil.rmtree(v.installationPath)
            except Exception as e:
              logger.error("Problems removing " + v.installationPath)
        writeAgdaDirFiles(True)
        logger.info(libname + " uninstalled")
        commit()

      except Expection as e:
        logger.error(e)
  commit()
