'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

from pathlib import Path

import click
import git
import subprocess

# ----------------------------------------------------------------------------

__author__ = "Jonathan Prieto-Cubides & Camilo Rodriguez"

# -----------------------------------------------------------------------------

# -- AGDA DIRECTORIES:
AGDA_DIR_PATH = Path().home().joinpath(".agda")
AGDA_DEFAULTS_PATH = AGDA_DIR_PATH.joinpath("defaults")
AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries")
AGDA_VERSION = ""

try:
  result = subprocess.run(["agda", "--version"], stdout=subprocess.PIPE)
  AGDA_VERSION = result.stdout.split()[2].decode()
  AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries-"+AGDA_VERSION)
except Exception(FileNotFoundError):
  print("Agda is not installed on this machine")

AGDA_PKG_PATH = Path().home().joinpath('.apkg' + ("@agda-" + AGDA_VERSION if len(AGDA_VERSION) > 0 else ""))
GITHUB_USER   = "apkgbot"

# The github repository index of all agda packages
INDEX_REPOSITORY_NAME = "package-index"
INDEX_REPOSITORY_URL = \
  "https://github.com/"+ GITHUB_USER + "/" + INDEX_REPOSITORY_NAME + ".git"
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
  # print("AGDA_PKG_PATH created at ", AGDA_PKG_PATH.as_posix())

if not INDEX_REPOSITORY_PATH.exists():
  INDEX_REPOSITORY_PATH.mkdir()
  # print("Package Index created at ", INDEX_REPOSITORY_PATH.as_posix())

if not PACKAGE_SOURCES_PATH.exists():
  PACKAGE_SOURCES_PATH.mkdir()
  # print("Package Sources created at ", INDEX_REPOSITORY_PATH.as_posix())

try:
  REPO = git.Repo.clone_from(INDEX_REPOSITORY_URL, INDEX_REPOSITORY_PATH)
except:
  REPO = git.Repo(INDEX_REPOSITORY_PATH)

if not DATABASE_FILE_PATH.exists():
  DATABASE_FILE_PATH.touch()

if not DATABASE_SEARCH_INDEXES_PATH.exists():
  DATABASE_SEARCH_INDEXES_PATH.mkdir()

if not AGDA_DIR_PATH.exists():
  AGDA_DIR_PATH.mkdir()
  # print("AGDA_DIR created at " + AGDA_DIR_PATH.as_posix())

  AGDA_DEFAULTS_PATH.touch()
  # print("defaults file created at " + AGDA_DEFAULTS_PATH.as_posix())

  AGDA_LIBRARIES_PATH.touch()
  # print("libraries file created at " + AGDA_LIBRARIES_PATH.as_posix())
