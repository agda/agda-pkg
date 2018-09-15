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
from ..service.sortVersions import sortVersions
from pprint   import pprint
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
@clog.simple_verbosity_option(logger)
@db_session
def uninstall(libname):
  library = Library.get(name = libname, installed = True)
  if library is not None:
    if click.confirm("Uninstalling... " + libname):
      try:
        library.installed = False
        library.default   = False
        for version in library.versions:
          version.installed = False
          if version.user_version:
            try:
              msg = "Delete all files in "+version.installation_path
              if click.confirm(msg):
                shutil.rmtree(version.installation_path)
            except Exception as e:
              logger.error("Problems removing " + version.installation_path)
        writeAgdaDirFiles(True)
        logger.info(libname + " uninstalled")
        commit()

      except Expection as e:
        logger.error(e)
  libraries = select(library for library in Library)[:]
  for library in libraries:
    print(library)
    versions = sortVersions(library.name)
    if len(versions) > 0:
      versions[-1].latest = True
  commit()
