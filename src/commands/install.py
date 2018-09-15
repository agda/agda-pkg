'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
import click
from pathlib import Path

from ..config import PACKAGE_SOURCES_PATH, INDEX_REPOSITORY_PATH

from ..service.readLibFile  import readLibFile
from ..service.sortVersions import sortVersions
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )
from ..service.writeAgdaDirFiles import writeAgdaDirFiles
from pprint   import pprint
from pony.orm import *
import uuid
from .uninstall import uninstall

import logging
import click_log as clog
# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def install():
  click.echo('[Clone]: initializing cloning')
  click.echo('[Clone]: repository successfully cloned')

@install.command()
@click.argument('libname')
@click.option('--src', type=str, default="", help='source code of the library')
@click.option('--version', type=str, default="", help='info of one version')
@click.option('--no-defaults', type=bool, default=False, help='do not installed as a default library')
@clog.simple_verbosity_option(logger)
@db_session
@click.pass_context
def install(ctx, libname, src, version, no_defaults):

  # local variables
  libFile = Path("")
  info = {}
  name = None
  versionName = None
  library = None
  versionLibrary = None

  if libname == ".":

    if version != "":
      logger.error("You can not use --version when installing local a local library")

    logger.info("Installation for user libraries")
    pathlib = Path().cwd().joinpath(Path(src))
    logger.info("Library location: " + pathlib.as_posix())

    agdaLibFiles = [ f for f in pathlib.glob("*.agda-lib") if f.is_file() ]
    agdaPkgFiles = [ f for f in pathlib.glob("*.agda-pkg") if f.is_file() ]

    agdaPkgFile = None

    # pkg has priority over lib files.

    if len(agdaLibFiles) == 0 and len(agdaPkgFiles) == 0:
      logger.error("No libraries (.agda-lib or .agda-pkg) files detected")
    elif len(agdaPkgFiles) == 1:
      libFile  = agdaPkgFiles[0]
    elif len(agdaLibFiles) == 1:
      libFile  = agdaLibFiles[0]
    else:
      logger.error("None or many agda libraries files.")
      return

    logger.info("Library file detected: " + libFile.name)
    info = readLibFile(libFile)

    name = info["name"]
    logger.info("Name: " + name)

    versionName = str(info["version"])
    logger.info("Version: " + versionName)

  library = Library.get(name=name)
  versionLibrary = LibraryVersion.get(library=library, name = versionName)

  if library is not None:
    if versionLibrary is not None:
      logger.warning(name + "@" + versionName +" is already installed.")
      versionName = str(info["version"]) +"-" + str(uuid.uuid1())
      logger.warning("Installing as " + name + "@" + versionName)
      if click.confirm('Do you want to continue?'):
        ctx.invoke(uninstall,libname=name)
      else:
        return
  else:
    library = Library(name = name)

  library.installed = True
  library.defaults = not(no_defaults)

  for v in library.versions:
    v.installed = False
    v.latest   = False

  # we may be using a new version
  versionLibrary = LibraryVersion.get(library=library, name = versionName)
  if versionLibrary is None:
    versionLibrary = LibraryVersion(library = library, name = versionName)
    versionLibrary.info_path = libFile.as_posix()

  versionLibrary.installation_path = pathlib.as_posix()
  versionLibrary.user_version = True
  versionLibrary.installed = True
  versionLibrary.latest = True

  commit()

  keywords = info.get("keywords", [])
  keywords += info.get("category", [])
  keywords = list(set(keywords))

  for word in keywords:
    keyword =  Keyword.get_for_update(word = word)
    if keyword is None:
      keyword = Keyword(word = word)

    keyword.libraries.add(library)
    keyword.libversions.add(versionLibrary)

  for depend in info["depend"]:
    if type(depend) == list:
      logger.info("no supported yet but the format is X.X <= name <= Y.Y")
    else:
      dependency = Library.get(name = depend)
      if dependency is not None:
        versionLibrary.requires.add(Dependency(library = dependency))
      else:
        logger.warning(depend + " is not in the index")
  commit()
  writeAgdaDirFiles(True)
