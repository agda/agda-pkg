'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import git
import subprocess
import os

from pathlib import Path

# -----------------------------------------------------------------------------

basedir = os.path.dirname(os.path.realpath(__file__))

# -- AGDA DIR:
AGDA_DIR_PATH = Path().home().joinpath(".agda")
if Path().cwd().joinpath(".agda").exists():
  AGDA_DIR_PATH = Path().cwd().joinpath(".agda")
if os.environ.get("AGDA_DIR", None) is not None:
  AGDA_DIR_PATH = Path(os.environ["AGDA_DIR"])

AGDA_DEFAULTS_PATH = AGDA_DIR_PATH.joinpath("defaults")
AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries")
AGDA_VERSION = os.environ.get("AGDA_VERSION","")

try:
  result = subprocess.run(["agda", "--version"], stdout=subprocess.PIPE)
  AGDA_VERSION = result.stdout.split()[2].decode()
  # # So far, Agda doesn't consider the commit, so we remove it.
  # AGDA_VERSION = AGDA_VERSION.split('-')[0]
  # AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries-%s"%AGDA_VERSION)
  # # TODO : I should report that agda is having problems reading libraries
  # #        from a file like "libraries-VERSION". Read the documentation.

except Exception as e:
  print("[!] Agda may not be installed on this machine!")
  print("    Please consider to install Agda v2.6.1+")

AGDA_PKG_PATH = Path().home().joinpath('.apkg' + \
                ("@agda-" + AGDA_VERSION if len(AGDA_VERSION) > 0 else ""))

GITHUB_USER   = "agda"
GITHUB_DOMAIN = "https://github.com/"
GITHUB_API    = "https://api.github.com/repos"

# The github repository index of all agda packages
INDEX_REPOSITORY_NAME = "package-index"
INDEX_REPOSITORY_URL = \
 GITHUB_DOMAIN + GITHUB_USER + "/" + INDEX_REPOSITORY_NAME + ".git"
INDEX_REPOSITORY_BRANCH = "master"
INDEX_REPOSITORY_PATH   = AGDA_PKG_PATH.joinpath(INDEX_REPOSITORY_NAME)

# this is folder where I keep all the source code for every library installed
PACKAGE_SOURCES_NAME = "package-sources"
PACKAGE_SOURCES_PATH = AGDA_PKG_PATH.joinpath(PACKAGE_SOURCES_NAME)

# We want to search fast queries using a database
DATABASE_FILE_NAME = INDEX_REPOSITORY_NAME + ".db"
DATABASE_FILE_PATH = AGDA_PKG_PATH.joinpath(DATABASE_FILE_NAME)
DATABASE_SEARCH_INDEXES_PATH = AGDA_PKG_PATH.joinpath("search-indexes")

REPO = None

PKG_SUFFIX = ".agda-pkg"
LIB_SUFFIX = ".agda-lib"

# -----------------------------------------------------------------------------

if not AGDA_PKG_PATH.exists():
  AGDA_PKG_PATH.mkdir()

if not INDEX_REPOSITORY_PATH.exists():
  INDEX_REPOSITORY_PATH.mkdir()

if not PACKAGE_SOURCES_PATH.exists():
  PACKAGE_SOURCES_PATH.mkdir()

try:
  REPO = git.Repo(INDEX_REPOSITORY_PATH, search_parent_directories=False)
except:
  try:
    REPO = git.Repo.clone_from(INDEX_REPOSITORY_URL, INDEX_REPOSITORY_PATH)
  except Exception as e:
    print(e)

if not DATABASE_FILE_PATH.exists():
  DATABASE_FILE_PATH.touch()

if not DATABASE_SEARCH_INDEXES_PATH.exists():
  DATABASE_SEARCH_INDEXES_PATH.mkdir()

if not AGDA_DIR_PATH.exists():
  AGDA_DIR_PATH.mkdir()
  AGDA_DEFAULTS_PATH.touch()
  AGDA_LIBRARIES_PATH.touch()

SUPPORT_FILES_PATH =(Path(basedir)/'support'/'nixos').resolve()
