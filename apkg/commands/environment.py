'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
from ..config             import ( AGDA_DEFAULTS_PATH
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
                                 , PACKAGE_SOURCES_PATH
                                 , PKG_SUFFIX
                                 , LIB_SUFFIX
                                 )
from ..service.logging   import logger, clog


# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def environment(): pass

@environment.command()
@clog.simple_verbosity_option(logger)
def environment():
  """Show environmental variables"""
  click.echo("AGDA_DEFAULTS_PATH: " + AGDA_DEFAULTS_PATH.as_posix())
  click.echo("AGDA_DIR_PATH: "+ AGDA_DIR_PATH.as_posix())
  click.echo("AGDA_LIBRARIES_PATH: "+ AGDA_LIBRARIES_PATH.as_posix())
  click.echo("AGDA_PKG_PATH: "+ AGDA_PKG_PATH.as_posix())
  click.echo("AGDA_VERSION: "+ AGDA_VERSION)
  click.echo("DATABASE_FILE_NAME: "+ DATABASE_FILE_NAME)
  click.echo("DATABASE_FILE_PATH: "+ DATABASE_FILE_PATH.as_posix())
  click.echo("DATABASE_SEARCH_INDEXES_PATH: "+ DATABASE_SEARCH_INDEXES_PATH.as_posix())
  click.echo("GITHUB_USER: "+ GITHUB_USER)
  click.echo("INDEX_REPOSITORY_BRANCH: "+ INDEX_REPOSITORY_BRANCH)
  click.echo("INDEX_REPOSITORY_NAME: "+ INDEX_REPOSITORY_NAME)
  click.echo("INDEX_REPOSITORY_PATH: "+ INDEX_REPOSITORY_PATH.as_posix())
  click.echo("INDEX_REPOSITORY_URL: "+ INDEX_REPOSITORY_URL)
  click.echo("PACKAGE_SOURCES_PATH: "+ PACKAGE_SOURCES_PATH.as_posix())
  click.echo("PKG_SUFFIX: "+ PKG_SUFFIX)
  click.echo("LIB_SUFFIX: "+ LIB_SUFFIX)
