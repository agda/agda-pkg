'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''


from pathlib import Path
import click
import git

__author__  = "Jonathan Prieto-Cubides & Camilo Rodriguez"

# -----------------------------------------------------------------------------

AGDA_PKG_PATH = Path().home().joinpath('.apkg')
GITHUB_USER   = "apkgbot"

# The github repository index of all agda packages
INDEX_REPOSITORY_NAME = "agda-packages"
INDEX_REPOSITORY_URL = \
  "https://github.com/"+ GITHUB_USER + "/" + INDEX_REPOSITORY_NAME + ".git"
INDEX_REPOSITORY_BRANCH = "master"
INDEX_REPOSITORY_PATH = AGDA_PKG_PATH.joinpath(INDEX_REPOSITORY_NAME)

# We want to search fast queries using a database
DATABASE_FILE_NAME   = INDEX_REPOSITORY_NAME + ".db"
DATABASE_FILE_PATH   = AGDA_PKG_PATH.joinpath(DATABASE_FILE_NAME)

# -----------------------------------------------------------------------------

if not AGDA_PKG_PATH.exists():
  AGDA_PKG_PATH.mkdir()
  print("Agda-Pkg directory: ", AGDA_PKG_PATH.as_posix())

if not INDEX_REPOSITORY_PATH.exists():
  INDEX_REPOSITORY_PATH.mkdir()
  print("Package Index directory: ", INDEX_REPOSITORY_PATH.as_posix())

try:
  REPO = git.Repo.clone_from(INDEX_REPOSITORY_URL, INDEX_REPOSITORY_PATH)
except:
  REPO = git.Repo(INDEX_REPOSITORY_PATH)

if not DATABASE_FILE_PATH.exists():
  DATABASE_FILE_PATH.touch()
  # run ponywhoosh...
