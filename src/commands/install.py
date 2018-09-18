'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
import click
import click_log as clog

import shutil
import uuid
import logging

from pathlib import Path
from pony.orm import *


from .uninstall import uninstall
from ..config import ( PACKAGE_SOURCES_PATH
                     , INDEX_REPOSITORY_PATH
                     )

from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )
from ..service.readLibFile       import readLibFile
from ..service.writeAgdaDirFiles import writeAgdaDirFiles
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
             , is_flag=True 
             , help='do not installed as a default library')
@click.option('--cache'
             , type=bool
             , is_flag=True 
             , help='install the cache version')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def install(ctx, libnames, src, version, no_defaults, cache):

  libnames = list(set(libnames))
  if len(libnames) == 0: libnames = ["."]
  if len(libnames) > 0 and version != "":
    logger.error("--version only works with one library, no more")
    return

  for libname in libnames:
    if libname != ".": logger.info("Installing... " + libname)
    else: logger.info("Installing local library...")

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
        logger.error("You can not use --version when installing a local library")
        return

      logger.info("Installating...")

      pwd = Path().cwd().joinpath(Path(src))
      logger.info("Library location: " + pwd.as_posix())

      agdaLibFiles = [ f for f in pwd.glob("*.agda-lib") if f.is_file() ]
      agdaPkgFiles = [ f for f in pwd.glob("*.agda-pkg") if f.is_file() ]

      # pkg has priority over lib files.

      if len(agdaLibFiles) == 0 and len(agdaPkgFiles) == 0:
        logger.error("No libraries (.agda-lib or .agda-pkg) files detected")
        return
        # -- TODO: offer the posibility to create a file agda-pkg!
      elif len(agdaPkgFiles) == 1:
        libFile  = agdaPkgFiles[0]
      elif len(agdaLibFiles) == 1:
        # -- TODO: offer the posibility ssto create a file agda-pkg!
        libFile  = agdaLibFiles[0]
      else:
        logger.error("None or many agda libraries files.")
        return

      logger.info("Library file detected: " + libFile.name)
      info = readLibFile(libFile)

      name = info["name"]
      logger.info("name: " + name)

      versionName = str(info["version"])
      if versionName == "": versionName = str(uuid.uuid1())
      logger.info("version: " + versionName)

    else:
      # Check first if the library is in the cache
      library = Library.get(name=libname)
      if library is not None:
        versionLibrary = None
        if version == "":
          versionLibrary = library.getLatestCachedVersion()
        else:
          versionLibrary = LibraryVersion(library=library, name=version, cached=True)
        if versionLibrary is not None:
          if versionLibrary.installed:
            logger.warning("This library is installed")
            return
          if click.confirm('Do you want to install the cached version?'):
            versionLibrary.install()
            writeAgdaDirFiles(True)
            return
          else:
            logger.error("No supported yet installation from the index")
            return
      else:
        logger.error("No supported yet installation from the index")
        return

    # At this point we have the name from the local library
    library = Library.get(name=name)
    if library is None and libname == "." :
      library = Library(name=name)

    versionLibrary = LibraryVersion.get(library=library, name=versionName)

    if versionLibrary is not None:
      if versionLibrary.installed:
        logger.warning("This version ({})) is already installed!"
                        .format(versionLibrary.freezeName))
        if click.confirm('Do you want to uninstall it first?'):
          ctx.invoke( uninstall
                    , libname=name
                    , remove_cache=True
                    )
        else:
          versionNameProposed = str(info["version"]) + "-" + str(uuid.uuid1())
          logger.warning("Renaming version to " + name + "@" + versionNameProposed)
          if click.confirm('Do you want to install it using this version?', abort=True):
            versionLibrary = LibraryVersion(library=library, name=versionNameProposed)
      else:
        if versionLibrary.sourcePath.exists():
          shutil.rmtree(versionLibrary.sourcePath)
    else:
      versionLibrary = LibraryVersion( library=library
                                     , name=versionName
                                     , cached=True
                                     )

    versionLibrary.fromIndex = False
    # we may be using a new version

    if libname == "." :
      # I should just copy the important content
      try:
        if versionLibrary.sourcePath.exists():
          versionLibrary.sourcePath.rmdir()
        shutil.copytree(Path().cwd().as_posix(), versionLibrary.sourcePath)
      except Exception as e:
        logger.error(e)
        logger.error("Fail to copy directory (" + Path().cwd().as_posix() + ")") 
        return
    commit()

    try:
      info = versionLibrary.readInfoFromLibFile()
      keywords = info.get("keywords", []) + info.get("category", [])
      keywords = list(set(keywords))

      for word in keywords:
        keyword = Keyword.get_for_update(word = word)
        if keyword is None:
          keyword = Keyword(word = word)
        
        if not library in keyword.libraries:
          keyword.libraries.add(library)
        if not versionLibrary in keyword.libVersions:
          keyword.libVersions.add(versionLibrary)

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
    except Exception as e:
      versionLibrary.sourcePath.rmdir()
      logger.error(e)
      logger.error("(1)")
      return 

    try:
      versionLibrary.install(not(no_defaults))
      writeAgdaDirFiles(True)
      commit()
    except Exception as e:
      versionLibrary.sourcePath.rmdir()
      logger.error(e)
      logger.error("(2)")
