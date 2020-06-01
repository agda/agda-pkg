'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click

import git
import humanize
import os
import random
import requests
import subprocess
import time
import uuid
import re

from distutils.dir_util  import copy_tree, remove_tree
from pathlib             import Path
from pony.orm            import db_session, commit
from tempfile            import TemporaryDirectory

from ..config            import ( PACKAGE_SOURCES_PATH
                                , INDEX_REPOSITORY_PATH
                                , PKG_SUFFIX
                                , GITHUB_DOMAIN 
                                , LIB_SUFFIX
                                , GITHUB_API
                                )

from ..service.database  import db
from ..service.database  import ( Library
                                , LibraryVersion
                                , Keyword
                                , Dependency
                                )

from ..service.logging            import logger, clog
from ..service.readLibFile        import readLibFile
from ..service.utils              import isURL, isGit, isIndexed, isLocal

from .uninstall                   import uninstallLibrary
from .write_defaults              import write_defaults

# ----------------------------------------------------------------------------
# -- Install command variants

# -- Command def.
@click.group()
def install(): pass

# -- Defaults

option = { 'branch'            : "master"
         , 'cache'             : False
         , 'editable'          : False
         , 'git'               : False
         , 'github'            : False
         , 'libnames'          : ()
         , 'libname'           : None
         , 'local'             : False
         , 'name'              : '*'
         , 'no_defaults'       : False
         , 'no_dependencies'   : False
         , 'requirement'       : None
         , 'src'               : ''
         , 'url'               : None
         , 'version'           : ''
         , 'yes'               : False
         , 'installing_depend' : False
         }

# ----------------------------------------------------------------------------

@db_session
def installFromLocal():
  
  global option

  if len(option["pathlib"]) == 0 or option["pathlib"] == ".":
    option["pathlib"] = Path().cwd()
  else:
    option["pathlib"] = Path(option["pathlib"])

  pwd = option["pathlib"].joinpath(Path(option["src"]))

  if not Path(pwd).exists():
    logger.error(pwd + " doesn't exist!")
    return None
  
  agdaLibFiles = [ f for f in pwd.glob(option["name"] + LIB_SUFFIX) if f.is_file() ]
  agdaPkgFiles = [ f for f in pwd.glob(option["name"] + PKG_SUFFIX) if f.is_file() ]

  if len(agdaLibFiles) + len(agdaPkgFiles) == 0:
    logger.error(" no libraries (" + LIB_SUFFIX + " or "\
                + PKG_SUFFIX + ") files detected." )
    return None
  
  libFile = Path("")
  if len(agdaPkgFiles) == 1:
    libFile = agdaPkgFiles[0]
  elif len(agdaLibFiles) == 1:
    libFile = agdaLibFiles[0]
  else:
    logger.error("[!] Use --name to specify the library name.")
    return None

  logger.info("Library file detected: " + libFile.name)
  
  info = readLibFile(libFile)

  option["name"] = info.get("name", "")

  if len(option["name"]) == 0:
    option["name"] = option["pathlib"].name

  versionName = option["version"]

  if versionName == "" :
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
    except: pass

  if versionName == "" and pwd.joinpath(".git").exists():
    try:
      with open(os.devnull, 'w') as devnull:
        result = subprocess.run( ["git", "rev-parse", "HEAD"]
                               , stdout=subprocess.PIPE
                               , stderr=devnull
                               , cwd=pwd.as_posix()
                               )
        versionName = result.stdout.decode()[:8]
    except: pass

  if versionName == "": 
    versionName = str(uuid.uuid1())

  logger.info("Library version: " + versionName)

  # At this point we have the name from the local library
  library = Library.get(name=option["name"])

  if library is None:
    library = Library( name=option["name"] )

  versionLibrary = LibraryVersion.get(library=library, name=versionName)

  if versionLibrary is not None:

    if versionLibrary.installed:
      logger.warning("This version ({}) is already installed."
                      .format(versionLibrary.freezeName))
      if option["yes"] or click.confirm('Do you want to uninstall it first?'):
        try:
          uninstallLibrary( libname=option["name"]
                          , database=False
                          , remove_cache=True
                          )
        except Exception as e:
          logger.error(e)
          return None
      else:
        
        versionNameProposed = "{}-{}".format(versionName, uuid.uuid1())
        logger.warning("Version suggested: " + option["name"] + "@" + versionNameProposed)

        if click.confirm('Do you want to install it using this version?', abort=True):
          versionLibrary = LibraryVersion( library=library
                                         , name=versionNameProposed
                                         , cached=True
                                         , editable=option["editable"]
                                         )
  else:
    versionLibrary = LibraryVersion( library=library
                                   , name=versionName
                                   , cached=True                  
                                   , editable=option["editable"]
                                   )
    
  if option["editable"]:
    versionLibrary.origin   = pwd.as_posix()
    versionLibrary.editable = True
    option["editable"]      = False  # Just used editable once

  try:
    if not(versionLibrary.editable):
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

      keyword = Keyword.get_for_update(word=word)

      if keyword is None:
        keyword = Keyword(word = word)
      
      if not library in keyword.libraries:
        keyword.libraries.add(library)

      if not versionLibrary in keyword.libVersions:
        keyword.libVersions.add(versionLibrary)

    versionLibrary.depend.clear()
    for depend in info.get("depend",[]):

      if type(depend) == list:
        logger.info("no supported yet.")
      else:
        if "@" in depend:
          dname, _ = depend.split("@")
        else:
          dname = depend
        dependency = Library.get(name=dname)

        if dependency is not None:
          versionLibrary.depend.add(Dependency(library=dependency))

          if not option["no_dependencies"] and not dependency.installed:

            oldOption          = option
            option["libname"]  = dependency.name
            option["version"]  = ""
            option["name"]     = "*"
            option["libnames"] = ()
            installFromIndex()
            option             = oldOption

        else:
          logger.warning(depend + " is not in the index")
    
    versionLibrary.install( not(option["no_defaults"]) )

    commit()
    return versionLibrary

  except Exception as e:
    try:
      if not(versionLibrary.editable) and versionLibrary.sourcePath.exists():
        remove_tree(versionLibrary.sourcePath.as_posix())
    except:
      logger.error(" fail to remove the sources: {}"
                  .format(versionLibrary.sourcePath.as_poasix())
                  )

    logger.error(e)
    return None


# ----------------------------------------------------------------------------
def installFromGit():

  global option

  if not isGit(option.get("url", "")):
    logger.error("This is not a git repository.\
                  You may want to add '.git' at the end of your URL.")
    return None
  
  logger.info("Installing from git: %s" % option["url"] )

  with TemporaryDirectory() as tmpdir:

    try:
      click.echo("Using temporary directory: {}".format(tmpdir))
      
      if Path(tmpdir).exists():
        remove_tree(tmpdir)

      # To display a nice progress bar, we need the size of
      # the repository, so let's try to get that number

      # -- SIZE Repo

      size = 0
      if "github" in option["url"]:

        reporef = option["url"].split("github.com")[-1]
        infourl = GITHUB_API + reporef.split(".git")[0]

        response = requests.get(infourl, stream=True)

        if not response.ok:
          logger.error("Request failed: %d" % response.status_code)
          return None

        info = response.json()
        size = int(info.get("size", 0))

      else:
        
        response = requests.get(option["url"], stream=True)
        if not response.ok:
          logger.error("Request failed: %d" % response.status_code)
          return None

        size_length = response.headers.get('content-length')
        size = 0
        if size_length is None:
          for _ in response.iter_content(1024):
              size += 1024
        else:
          size = size_length
        size = int(size)

      logger.info("Downloading " + option["url"]  \
            + " (%s)" % str(humanize.naturalsize(size, binary=True)))
      
      with click.progressbar( length=10*size
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

            bar.update(self.total)

        click.echo("Git branch: " + option["branch"])

        REPO = git.Repo.clone_from( option["url"]
                                  , tmpdir
                                  , branch=option["branch"]
                                  , progress=Progress()
                                  )

      if option["version"] != "":
        try:
          # Seen on https://goo.gl/JVs8jJ
          REPO.git.checkout(option["version"])

        except Exception as e:
          logger.error(e)
          logger.error(" version or tag not found ({})".format(option["version"]))
          return None

      option["pathlib"] = tmpdir

      libVersion = installFromLocal()

      if libVersion is None:
        logger.error(" we couldn't install the version you specified.")
        return None

      libVersion.fromGit = True
      libVersion.origin = option["url"]
      libVersion.library.url = option["url"]
      libVersion.library.default = not(option["no_defaults"])

      if option["version"] != "": 
        libVersion.sha = REPO.head.commit.hexsha
        
      commit()
      return libVersion

    except Exception as e:
      logger.error(e)
      logger.error("There was an error when installing the library. May you want to run init?")
      return None

# ----------------------------------------------------------------------------
@db_session
def installFromIndex():

  global option

  if len(option["libname"]) == 0:
    logger.info("Nothing to install.")
    return

  if "@" in option["libname"]:
    option["libname"], option["version"] = option["libname"].split("@")
  elif "==" in option["libname"]:
    option["libname"], option["version"] = option["libname"].split("==")

  # Check first if the library is in the cache
  logger.info("Installing ({}) from the index...".format(option["libname"]))
  library = Library.get(name=option["libname"])

  if library is not None:

    versionLibrary = None

    if option["version"] == "":
      # we'll try to install the latest git version
      versionLibrary = library.getLatestVersion()
      option["version"] = versionLibrary.name

    else:
      versionLibrary = LibraryVersion.get( library=library
                                         , name=option["version"]
                                         , fromIndex=True
                                         , fromGit=True
                                         )
      if versionLibrary is None and \
        option["version"] != "" and \
        not(option["version"].startswith("v")):
        # try with 

        versionLibrary = LibraryVersion.get( library=library
                                   , name= "v" + option["version"]
                                   , fromIndex=True
                                   , fromGit=True
                                   )
        if versionLibrary is not None:
          versionLibrary.name = "v" + option["version"]
    
    if versionLibrary is None:
      if option["version"] != "":
        logger.error(" the version (" + option["version"] +") is not available in the index.")
      else:
        logger.error(" no versions for this library. Please initialize the index.")
      return None
    
    if versionLibrary.installed:
      logger.info("Requirement already satisfied.")
      return versionLibrary

    elif versionLibrary.cached and \
      (option["yes"] or click.confirm('Do you want to install the cached version?')):
        versionLibrary.install()
        return versionLibrary

    else:
      option["url"]    = versionLibrary.library.url
      option["branch"] = "master"

      versionLibrary = installFromGit()

      if versionLibrary is not None:
        versionLibrary.fromIndex = True
        versionLibrary.cached    = True

      return versionLibrary
  else:
    logger.error("Library not available.")
    return None

# ----------------------------------------------------------------------------
def installFromURL():
  return None

# ----------------------------------------------------------------------------
@install.command()
@click.argument('libnames', nargs=-1)
@click.option('--src'
             , type=str
             , default=option["src"]
             , help='Directory to the source.')
@click.option('--version'
             , type=str
             , default=option["version"]
             , help='Version, tag or commit.')
@click.option('--no-defaults'
             , type=bool
             , is_flag=True 
             , help='No default library.')
@click.option('--cache'
             , type=bool
             , is_flag=True
             , default=option["cache"]
             , help='Cache available.')
@click.option('--editable'
             , type=bool
             , is_flag=True
             , default=option["editable"]
             , help='Install a local library in editable mode')
@click.option('--local'
             , type=bool
             , is_flag=True 
             , help='Force to install just local packages.')
@click.option('--name'
             , type=str
             , help='Help to disambiguate when many library files exist\
                    in the same directory.')
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
             , type=str
             , default="master"
             , help='From a git repository.')
@click.option('--no-dependencies'
             , type=bool
             , is_flag=True 
             , help='Do not install dependencies.')
@click.option('-r'
             , '--requirement'
             , type=click.Path(exists=True)
             , help='Use a requirement file.')
@click.option('--yes'
             , type=bool
             , is_flag=True 
             , help='Yes for everything.')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def install( ctx, libnames, src, version, no_defaults
           , cache, editable, local, name, url, git, github, branch
           , no_dependencies,requirement, yes):

  """Install one or more packages."""

  global option 

  option.update({k : v for k, v in ctx.__dict__["params"].items()
                     if v is not None} )

  option["libnames"] = list(set(libnames))

  if requirement:
    try:
      option["libnames"] += Path(requirement).read_text().split()
    except Exception as e:
      logger.error(e)
      logger.error(" installation failed.")
      return

  if len(option["libnames"]) > 1 and option["version"] != "":
    return logger.error("--version option only works for one library.\n\
      Please consider to use nameLibrary@versionNumber.")

  if (option["git"] or option["github"]) and option["url"]:
    return logger.error("--git and --url are incompatible")

  if len(option["libnames"]) == 0:
    option["libnames"] = ["."]

  if option["github"]: 
    option["git"]    = True
    option["github"] = True

  for libname in option["libnames"]:

    if "@" in libname:
      option["libname"], option["version"] = libname.split("@")
    elif "==" in libname:
      option["libname"], option["version"] = libname.split("==")
    else:
      option["libname"] = libname

    if option["github"]: 
      if not option["libname"].startswith(GITHUB_DOMAIN):
        option["libname"] = GITHUB_DOMAIN + option["libname"]
      if not option["libname"].endswith(".git"):
        option["libname"] = option["libname"] + ".git"

    option["pathlib"] = option["libname"]
    option["url"]     = option["libname"]

    vLibrary = None

    try:  

      if option["local"]:
        vLibrary = installFromLocal()

      elif isIndexed(option["libname"]):
        vLibrary = installFromIndex()

      elif git or isGit(option["libname"]):
        vLibrary = installFromGit()

      elif isLocal(option["pathlib"]):
        vLibrary = installFromLocal()

    except Exception as e:
      logger.error("Unsuccessfully installation {}."
                  .format(option["libname"] if name =="*" else name))
      continue
    
    if vLibrary is not None:
      logger.info("Successfully installed ({}@{})."
        .format(vLibrary.library.name, vLibrary.name))
      logger.info("\tSource code available on: {}"
        .format(vLibrary.sourcePath))
    else:
      logger.info("Unsuccessfully installation ({}).".format(option["libname"]))

  ctx.invoke(write_defaults, yes = yes)
