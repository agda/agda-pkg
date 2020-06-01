'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
import shutil

from pathlib             import Path

from ..config            import AGDA_PKG_PATH, AGDA_DIR_PATH
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

rmdirs = [ AGDA_PKG_PATH , AGDA_DIR_PATH ]
msg1 = ('\n  '.join(map(lambda x : x.as_posix(), rmdirs)))
promptMessage = 'Directories:\n  ' + msg1 + '\nDo you really want to remove these directories?'

# -- Command def.
@click.group()
def clean(): pass

@clean.command()
@click.confirmation_option(prompt=promptMessage)
@clog.simple_verbosity_option(logger)
def clean():
  """Remove the directories used by Agda-Pkg."""

  for dir in rmdirs:
    try:
      shutil.rmtree(dir)
      logger.info(dir.as_posix() + " (deleted)")
    except Exception as e:
      logger.error(e)
