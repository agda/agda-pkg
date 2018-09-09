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
def info():
    pass

@info.command()
@click.argument('libname')
@click.option('--version', '-v', type=str, default="", help='show information of a specific version')
@click.option('--field', '-f', type=str, default= help='show information of a specific field')
@db_session
def info(libname, version, field):
  """Working ..."""
  if version == "":
    lib = Library.get(name = libname)
    if lib is None:
      print("No available")
      return
    versions = [ v for v in lib.versions ]
    lastversion = versions[0]
    assert lastversion is not None
    info = readLibFile(lastversion.info_path)
    if field != "":
      if field in info:
        click.echo(info[field])
      else:
        click.echo("No information about " + field)
    else:
      for k, v in info.items():
        if k is "version": pass
        if (type(v) == str or type(v) == list) and len(v) > 0:
          click.echo("{0}: {1}".format(k, v))

    if len(versions) > 0:
      click.echo("Versions available:")
      for v in versions:
        ms = "  - %s" % v.name + ("Installed!" if v.installed else "")
        click.echo(ms)
