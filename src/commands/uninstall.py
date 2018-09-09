'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from pathlib import *

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
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pprint   import pprint
from pony.orm import *

@click.group()
def uninstall():
  pass

@uninstall.command()
@click.argument('libname')
@db_session
def uninstall(libname):
  library = Library.get(name = libname, installed = True)
  if library is None:
    click.echo(libname + " is not installed")
  else:
    # revisar si rompe algo y avisar!
    # preguntar y/n

    library.installed = False
    for version in library.versions:
      version.installed = False
