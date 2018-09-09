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
def freeze():
    pass

@freeze.command()
@db_session
def freeze():
  libraries = select(l for l in Library if l.installed)[:]
  for library in libraries:
    versions = [v for v in library.versions if v.installed]
    assert len(versions) == 1
    installedVersion = versions[0]
    click.echo(library.name + "==" + installedVersion.name)
