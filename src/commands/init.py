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
                     , DATABASE_SERACHINDEXES_PATH
                     , GITHUB_USER
                     , INDEX_REPOSITORY_BRANCH
                     , INDEX_REPOSITORY_NAME
                     , INDEX_REPOSITORY_PATH
                     , INDEX_REPOSITORY_URL
                     , LEGACY_MODE
                     , REPO
                     )

from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from ..service.readLibFile import readLibFile
from pprint import pprint
from pony.orm import *

@click.group()
def init():
	pass

@init.command()
@db_session
def init():
  f = INDEX_REPOSITORY_PATH
  src = f.joinpath("src")
  for lib in src.glob("*"):
    name = lib.name
    print(name)
    print("="* (len(name) + 1))

    url = Path(lib).joinpath("url").read_text()
    print("- URL: " + url,)

    print("- Versions:")
    for version in lib.joinpath("versions").glob("*"):
      valid = False
      print( "  " + ("- [x]" if valid else "- [ ]") + " v"+(version.name)+"")

      info = {}
      agdaLibFile = version.joinpath(name +".agda-lib")
      agdaPkgFile = version.joinpath(name +".agda-pkg")
      if agdaLibFile.exists():
        info = readLibFile(agdaLibFile)
      if agdaPkgFile.exists():
        info = readLibFile(agdaPkgFile)
      if info == {}:
        print("ERROR reading description file")
    print("\n")
