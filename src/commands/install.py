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
from urllib.parse import urlparse

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

# -- Some tests
def isURL(url):
  min_attr = ('scheme' , 'netloc')
  try:
    result = urlparse(url)
    # -- TODO : improve this test checking if it's available
    return all([result.scheme, result.netloc])
  except:
    return False

def isGit(url):
  min_attr = ('scheme' , 'netloc')
  try:
    result = urlparse(url)
    netloc = result.netloc
    # -- TODO : improve this test using gitpython
    return all([result.scheme, result.netloc]) and netloc.endswith(".git")
  except:
    return False

@db_session
def isIndexed(libname):
  return Library.get(name=libname) is not None

def isLocal(path):
  return Path(path).exists()

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# ----------------------------------------------------------------------------
# -- Install command variants

# -- Command def.
@click.group()
def install(): pass

# ----------------------------------------------------------------------------
@db_session
def installFromIndex(libname, src, version, no_defaults, cache):
  # Check first if the library is in the cache
  logger.info("Installing from the index...")
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

# ----------------------------------------------------------------------------
@db_session
def installFromLocal(libname, src, version, no_defaults, cache):
  # check
  # libname is . or is a directory in the filesystem 
  logger.info("Installing from a local package...")
  assert Path(libname).exists(), libname + " doesn't exist!"

  libFile = Path("")
  info = {}
  name = None
  versionName = None
  library = None
  versionLibrary = None

  pwd = Path().cwd().joinpath(Path(src))
  logger.info("Library location: " + pwd.as_posix())

  agdaLibFiles = [ f for f in pwd.glob("*.agda-lib") if f.is_file() ]
  agdaPkgFiles = [ f for f in pwd.glob("*.agda-pkg") if f.is_file() ]

  # # pkg has priority over lib files.

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
          versionLibrary = LibraryVersion( library=library
                                         , name=versionNameProposed)
    else:
      if versionLibrary.sourcePath.exists():
        shutil.rmtree(versionLibrary.sourcePath)
  else:
    versionLibrary = LibraryVersion( library=library
                                   , name=versionName
                                   , cached=True
                                   )

  versionLibrary.fromIndex = False

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

# ----------------------------------------------------------------------------
def installFromURL(url, src, version, no_defaults, cache):
  logger.info("Installing from url: %s" % url )


# ----------------------------------------------------------------------------
def installFromGit(url, src, version, no_defaults, cache, branch):
  logger.info("Installing from git: %s" % url )

# ----------------------------------------------------------------------------
@install.command()
@click.argument('libnames', nargs=-1)
@click.option('--src'
             , type=str
             , default=""
             , help='source code of the library')
@click.option('--version'
             , type=str
             , default=""
             , help='version or commit if you use --git')
@click.option('--no-defaults'
             , type=bool
             , is_flag=True 
             , help='do not installed as a default library')
@click.option('--cache'
             , type=bool
             , is_flag=True 
             , help='install the cache version')
@click.option('--url'
             , type=bool
             , is_flag=True 
             , help='from a url address')
@click.option('--git'
             , type=bool
             , is_flag=True 
             , help='from a git repository')
@click.option('--branch'
             , type=bool
             , is_flag=True 
             , help='from a git repository')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def install(ctx, libnames, src, version, no_defaults, cache, url, git, branch):

  libnames = list(set(libnames))

  if len(libnames) > 1 and version != "":
    return logger.error("--version only works with one library, no more")
  
  if git and url:
    return logger.error("--git and --url are incompatible")

  if len(libnames) == 0: libnames = ["."]

  for libname in libnames:
    try:
      if git and isGit(libname):
        installFromGit(libname, src, version, no_defaults, cache, branch)
      elif url and isURL(libname):
        installFromURL(libname, src, version, no_defaults, cache)
      elif isLocal(libname):
        installFromLocal(libname, src, version, no_defaults, cache)
      elif isIndexed(libname):
        installFromIndex(libname, src, version, no_defaults, cache)
    except Exception as e:
      logger.error(e)
      logger.error("we can not install " + libname)
