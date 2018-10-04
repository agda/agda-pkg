'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
import shutil

from pathlib             import Path

from ..config            import AGDA_PKG_PATH,AGDA_DIR_PATH
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def clean(): pass

@clean.command()
@clog.simple_verbosity_option(logger)
def clean():
  """Remove the directories used by apkg."""
  rmdirs = [ AGDA_PKG_PATH , AGDA_DIR_PATH ]
  for dir in rmdirs:
    try:
      shutil.rmtree(dir)
      logger.info(dir.as_posix() + " (deleted)")
    except Exception as e:
      logger.error(e)
