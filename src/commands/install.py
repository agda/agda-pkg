'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
import click
from pathlib import Path

from ..config import PACKAGE_SOURCES_PATH, INDEX_REPOSITORY_PATH

from ..service.readLibFile  import readLibFile
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )
from ..service.writeAgdaDirFiles import writeAgdaDirFiles
from pony.orm import *
import uuid
import shutil
from .uninstall import uninstall

import logging
import click_log as clog
# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def install(): pass

@install.command()
@click.argument('libnames', nargs=-1)
@click.option('--src'
             , type=str
             , default=""
             , help='source code of the library')
@click.option('--version'
             , type=str
             , default=""
             , help='info of one version')
@click.option('--no-defaults'
             , type=bool
             , default=False
             , help='do not installed as a default library')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def install(ctx, libnames, src, version, no_defaults):

  libnames = list(set(libnames))
  if len(libnames) == 0: libnames = ["."]

  for libname in libnames:
    if libname != ".": logger.info("Installing... " + libname)

    # local variables
    libFile = Path("")
    info = {}
    name = None
    versionName = None
    library = None
    versionLibrary = None

    # A local package
    if libname == ".":

      if version != "":
        logger.error("You can not use --version when installing local a local library")
        return

      logger.info("Installation for user libraries")
      pathlib = Path().cwd().joinpath(Path(src))
      logger.info("Library location: " + pathlib.as_posix())

      agdaLibFiles = [ f for f in pathlib.glob("*.agda-lib") if f.is_file() ]
      agdaPkgFiles = [ f for f in pathlib.glob("*.agda-pkg") if f.is_file() ]

      # pkg has priority over lib files.

      if len(agdaLibFiles) == 0 and len(agdaPkgFiles) == 0:
        logger.error("No libraries (.agda-lib or .agda-pkg) files detected")
        return
        # -- TODO: offer the posibility to create a file agda-pkg!
      elif len(agdaPkgFiles) == 1:
        libFile  = agdaPkgFiles[0]
      elif len(agdaLibFiles) == 1:
        # -- TODO: offer the posibility to create a file agda-pkg!
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
    versionLibrary = None

    if library is not None:
      logger.info("Library name exists")
      versionLibrary = LibraryVersion.get(library=library, name = versionName)
      if versionLibrary is not None:
        logger.info("Library Version exists")
        logger.warning(name + "@" + versionName +" is already installed.")
        versionName = str(info["version"]) +"-" + str(uuid.uuid1())
        logger.warning("The new name is " + name + "@" + versionName)
        if click.confirm('Do you want to continue?'):
          ctx.invoke(uninstall,libname=name)
        else:
          return
    else:
      library = Library(name = name)

    library.installed = True
    library.default = not(no_defaults)

    for v in library.versions:
      v.installed = False
      v.latest    = False

    # we may be using a new version
    versionLibrary = LibraryVersion.get(library=library, name = versionName)
    if versionLibrary is None:
      versionLibrary = LibraryVersion(library = library, name = versionName)

    locationName = library.name + "@" + versionName
    versionLibrary.user_version = True
    versionLibrary.installed    = True

    versionLibrary.info_path = (PACKAGE_SOURCES_PATH
                               .joinpath(locationName)
                               .joinpath(libFile.name)
                               .as_posix())
    versionLibrary.installationPath = (PACKAGE_SOURCES_PATH
                                       .joinpath(locationName)
                                       .as_posix())

    if Path(versionLibrary.installationPath).exists():
      Path(versionLibrary.installationPath).rmdir()

    if libname == "." :
      # I should just copy the important content
      try:
        shutil.copytree(Path().cwd().as_posix(), versionLibrary.installationPath)
      except Exception as e:
        logger.error(e)
        logger.error("Fail to copy directory..." + Path().cwd().as_posix())
        return

    commit()

    keywords = info.get("keywords", []) + info.get("category", [])
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
          versionLibrary.depend.add(Dependency(library = dependency))
        else:
          logger.warning(depend + " is not in the index")
    commit()
    writeAgdaDirFiles(True)
