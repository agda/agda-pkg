'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
import click_log as clog

import git
import humanize
import logging
import os
import random
import requests
import subprocess
import time
import uuid

from distutils.dir_util  import copy_tree, remove_tree
from pathlib             import Path
from pony.orm            import *
from tempfile            import *
from urllib.parse        import urlparse


from ..config            import ( PACKAGE_SOURCES_PATH
                                , INDEX_REPOSITORY_PATH
                                , PKG_SUFFIX
                                , GITHUB_DOMAIN 
                                , LIB_SUFFIX
                                )

from ..service.database  import db
from ..service.database  import ( Library
                                , LibraryVersion
                                , Keyword
                                , Dependency
                                )

from ..service.readLibFile       import readLibFile
from ..service.writeAgdaDirFiles import writeAgdaDirFiles
from .uninstall                  import uninstallLibrary

# ----------------------------------------------------------------------------

# -- Some tests -- TODO: move these to some util module outside.
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
    return all([result.scheme, result.netloc]) and result.path.endswith(".git")
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
def installFromLocal(pathlib, name, src, version, no_defaults, cache):
  # logger.info("Installing as a local package...")

  if len(pathlib) == 0 or pathlib == ".":
    pathlib = Path().cwd()
  else:
    pathlib = Path(pathlib)

  pwd = pathlib.joinpath(Path(src))

  if not Path(pwd).exists():
    logger.error(pwd + " doesn't exist!")
    return None
  
  # logger.info("Library location: " + pwd.as_posix())

  agdaLibFiles = [ f for f in pwd.glob(name + LIB_SUFFIX) if f.is_file() ]
  agdaPkgFiles = [ f for f in pwd.glob(name + PKG_SUFFIX) if f.is_file() ]

  if len(agdaLibFiles) == 0 and len(agdaPkgFiles) == 0:
    logger.error("No libraries ("+LIB_SUFFIX+" or "+PKG_SUFFIX+") files detected.")
    return None

  libFile = Path("")
  
  # -- TODO: offer the posibility to create a file agda-pkg!
  if len(agdaPkgFiles) == 1:
    libFile = agdaPkgFiles[0]
  elif len(agdaLibFiles) == 1:
    # -- TODO: offer the posibility ssto create a file agda-pkg!
    libFile = agdaLibFiles[0]
  else:
    logger.error("None or many agda libraries files.")
    logger.info("[!] Use --name to specify the library name.")
    return None

  logger.info("Library file detected: " + libFile.name)
  info = readLibFile(libFile)

  name = info.get("name", "")
  if len(name) == 0:
    name = pathlib.name
  # logger.info("Library name: " + name)

  # -- Let's attach a version number

  versionName = version

  if versionName == "":
    versionName = str(info.get("version", ""))
  if versionName == "" and pwd.joinpath(".git").exists():
    try:
      with open(os.devnull, 'w') as devnull:
        result = subprocess.run( ["git", "describe", "--tags", "--long"]
                               , stdout=subprocess.PIPE
                               , stderr=devnull
                               , cwd=pwd.as_posix()
                               )
        versionName = result.stdout.decode()
    except:
      pass

  if versionName == "" and pwd.joinpath(".git").exists():
    try:
      with open(os.devnull, 'w') as devnull:
        result = subprocess.run( ["git", "rev-parse", "HEAD"]
                               , stdout=subprocess.PIPE
                               , stderr=devnull
                               , cwd=pwd.as_posix()
                               )
        versionName = result.stdout.decode()[:8]
    except:
      pass

  if versionName == "": 
    versionName = str(uuid.uuid1())

  logger.info("Library version: " + versionName)

  # At this point we have the name from the local library
  library = Library.get(name=name)

  if library is None:
    library = Library(name=name)

  versionLibrary = LibraryVersion.get(library=library, name=versionName)

  if versionLibrary is not None:

    if versionLibrary.installed:
      logger.warning("This version ({})) is already installed!"
                      .format(versionLibrary.freezeName))
      if click.confirm('Do you want to uninstall it first?'):
        uninstallLibrary(libname=name, database=True, remove_cache=True)
      else:
        versionNameProposed = str(info["version"]) + "-" + str(uuid.uuid1())
        logger.warning("Renaming version to " + name + "@" + versionNameProposed)
        if click.confirm('Do you want to install it using this version?', abort=True):
          versionLibrary = LibraryVersion( library=library
                                         , name=versionNameProposed
                                         )
    else:
      if versionLibrary.sourcePath.exists():
        logger.warning("[!] removing tree 1.")
        remove_tree(versionLibrary.sourcePath.as_posix())
  else:
    versionLibrary = LibraryVersion( library=library
                                   , name=versionName
                                   , cached=True
                                   )

  try:
    if versionLibrary.sourcePath.exists():
      remove_tree(versionLibrary.sourcePath.as_posix())

    logger.info("Adding " + versionLibrary.sourcePath.as_posix())
    copy_tree(pwd.as_posix(), versionLibrary.sourcePath.as_posix())

  except Exception as e:
    logger.error(e)
    logger.error("Fail to copy directory (" + pwd.as_posix() + ")") 
    return None
    
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

    for depend in info.get("depend",[]):
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
    try:
      remove_tree(versionLibrary.sourcePath.as_posix())
    except:
      logger.error(" fail to remove the sources:" + versionLibrary.sourcePath.as_posix())

    logger.error(e)
    logger.warning("[!] removing tree 3.")
    return None

  try:
    versionLibrary.install(not(no_defaults))
    writeAgdaDirFiles(False)
    commit()
    return versionLibrary

  except Exception as e:
    if versionLibrary.sourcePath.exists():
      remove_tree(versionLibrary.sourcePath.as_posix())
      logger.warning("[!] removing tree." + versionLibrary.sourcePath.as_posix())
    logger.error(e)
  return None

# ----------------------------------------------------------------------------
def installFromGit(url, name, src, version, no_defaults, cache, branch):

  logger.info("Installing from git: %s" % url )

  if not isGit(url):
    logger.error("this is not a git repository")
    return None

  # tmpdirname = "/tmp/qwerty"
  # if True:
  with TemporaryDirectory() as tmpdirname:
    print("Using temporal directory:", tmpdirname)
    try:
      if branch is None: branch = "master"
      if Path(tmpdirname).exists():
        remove_tree(tmpdirname)

      # To display a nice progress bar, we need the size of
      # the repository, so let's try to get that number

      # --
      size = 0
      if "github" in url:
        reporef = url.split("github.com")[-1]
        infourl = "https://api.github.com/repos" + reporef.split(".git")[0]
        # print(url)
        response = requests.get(infourl, stream=True)
        if not response.ok:
          logger.error("Request failed: %d" % response.status_code)
          return None
        info = response.json()
        size = int(info.get("size", 0))
      else:
        response = requests.get(url, stream=True)
        if not response.ok:
          logger.error("Request failed: %d" % response.status_code)
          return None

        size_length = response.headers.get('content-length')
        size = 0
        if size_length is None:
          for block in response.iter_content(1024):
              size += 1024
        else:
          size = size_length
        size = int(size)
      # --

      logger.info("Downloading " + url  + " (%s)" % str(humanize.naturalsize(size, binary=True)))
      
      with click.progressbar(
            length=10*size
          # , label = ""
          , bar_template='|%(bar)s| %(info)s %(label)s'
          , fill_char=click.style('█', fg='cyan')
          , empty_char=' '
          , width=30
          ) as bar:

        class Progress(git.remote.RemoteProgress):
          
          total, past = 0 , 0

          def update(self, op_code, cur_count, max_count=None, message=''):

            if cur_count < 10:
              self.past = self.total
            self.total = self.past + int(cur_count)
            # time.sleep(0.1 * random.random())
            bar.update(self.total)
            # click.echo("{}/{}".format(self.total, size))

        REPO = git.Repo.clone_from(url, tmpdirname, branch=branch, progress=Progress())

      if version != "":
        try:
          # Seen on https://goo.gl/JVs8jJ
          REPO.git.checkout(version)

        except Exception as e:
          logger.error(e)
          logger.error(" version or tag not found ({})".format(version))
          return None

      # else:
        # version = REPO.head.commit.hexsha

      libVersion = installFromLocal(tmpdirname, name, src, version, no_defaults, cache)

      if libVersion is None:
        raise ValueError(" we couldn't install the version you specified.")

      libVersion.fromGit = True
      libVersion.origin = url
      libVersion.library.url = url
      libVersion.library.default = not(no_defaults)

      if version != "":
        # libVersion.name = version
        libVersion.sha = REPO.commit()

      commit()
      writeAgdaDirFiles(False)
      return libVersion

    except Exception as e:
      logger.error(e)
      logger.error("Problems to install the library,\n\
                    May you want to run $ apkg init?")
      return None

# ----------------------------------------------------------------------------
@db_session
def installFromIndex(libname, src, version, no_defaults, cache):

  # Check first if the library is in the cache
  # logger.info("Installing from the index...")
  library = Library.get(name=libname)

  if library is not None:

    versionLibrary = None
    if version == "":
      # we'll try to install the latest git version
      for v in library.getSortedVersions():
        if v.fromGit and v.fromIndex:
          versionLibrary = v
          version = versionLibrary.name
          break
    else:
      versionLibrary = LibraryVersion.get( library=library
                                     , name=version
                                     , fromIndex=True
                                     , fromGit=True
                                     )
    
    if versionLibrary is None:
      logger.error(" no versions for this library.\n\
                    Index may be corrupted. Try $ apkg init")
      return None
    
    if versionLibrary.installed:
      logger.info("Requirement already satisfied.")
      return versionLibrary

    elif versionLibrary.cached and \
      click.confirm('Do you want to install the cached version?'):
        versionLibrary.install()
        writeAgdaDirFiles()
        return versionLibrary

    else:
      url = versionLibrary.library.url
      versionLibrary = installFromGit(url, libname, src, version
                                     , no_defaults, cache, "master")
      if versionLibrary is not None:
        versionLibrary.fromIndex = True
        versionLibrary.cached    = True

      return versionLibrary
  else:
    logger.error("Library not available.")
    return None

# ----------------------------------------------------------------------------
def installFromURL(url, name, src, version, no_defaults, cache):
  logger.info("Command not available yet")
  return None

# ----------------------------------------------------------------------------
@install.command()
@click.argument('libnames', nargs=-1)
@click.option('--src'
             , type=str
             , default=""
             , help='Directory to the source.')
@click.option('--version'
             , type=str
             , default=""
             , help='Version, tag or commit.')
@click.option('--no-defaults'
             , type=bool
             , is_flag=True 
             , help='No default library.')
@click.option('--cache'
             , type=bool
             , is_flag=True
             , default=True
             , help='Cache available.')
@click.option('--local'
             , type=bool
             , is_flag=True 
             , help='Force to install just local packages.')
@click.option('--name'
             , type=str
             , default="*"
             , help='Help to disambiguate when many lib files are\
                     present in the directory.')
@click.option('--url'
             , type=bool
             , is_flag=True 
             , help='From a url address.')
@click.option('--git'
             , type=bool
             , is_flag=True 
             , help='From a git repository.')
@click.option('--github'
             , type=bool
             , is_flag=True 
             , help='From a github repository.')
@click.option('--branch'
             , type=bool
             , is_flag=True 
             , help='From a git repository.')
@click.option('-r'
             , '--requirement'
             , type=click.Path(exists=True)
             , help='Use a requirement file.')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def install( ctx, libnames, src, version, no_defaults \
           , cache, local, name, url, git, github, branch,requirement):
  """Install packages."""

  libnames = list(set(libnames))

  if requirement:
    try:
      rfile = Path(requirement)
      libnames += rfile.read_text().split()
    except Exception as e:
      logger.error(e)
      logger.error(" installation failed.")
      return


  if len(libnames) > 1 and version != "":
    return logger.error("--version only works with one library.\n\
      Consider using nameLibrary@versionNumber instead.")
  
  if (git or github) and url:
    return logger.error("--git and --url are incompatible")

  if len(libnames) == 0: libnames = ["."]

  if github: git = True

  for libname in libnames:

    if "@" in libname:
      libname, version = libname.split("@")
    elif "==" in libname:
      libname, version = libname.split("==")

    if github: 
      if not libname.starswith(GITHUB_DOMAIN):
        libname = GITHUB_DOMAIN + libname
      if not libname.endswith(".git"):
        libname = libname + ".git"

    pathlib  = libname
    url      = libname
    vLibrary = None

    try:  
      if local:
        vLibrary = installFromLocal(pathlib,name,src,version,no_defaults,cache)
      elif isIndexed(libname):
        vLibrary = installFromIndex(libname,src,version,no_defaults,cache)
      elif git or isGit(libname):
          Library = installFromGit(url,name,src,version,no_defaults,cache,branch)
      elif isLocal(pathlib):
        vLibrary =  installFromLocal(pathlib,name,src,version,no_defaults,cache)

    except Exception as e:
      logger.error("Unsuccessfully installation ({}@{})."
                  .format(libname if name =="*" else name, version))
      continue
    
    if vLibrary is not None:
      logger.info("Successfully installed ({}@{})."
                 .format(libname if name =="*" else name, vLibrary.name))
    else:
      logger.info("Unsuccessfully installation ({})."
                 .format(libname if name =="*" else name))

  writeAgdaDirFiles()
