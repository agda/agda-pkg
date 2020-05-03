'''
  apkg
  ~~~~

  A package manager for Agda.

'''


# ----------------------------------------------------------------------------

import click
import os

from pathlib             import Path
from distutils.dir_util  import copy_tree

from ..config            import ( AGDA_VERSION
                                , LIB_SUFFIX
                                , PKG_SUFFIX
                                , SUPPORT_FILES_PATH
                                )
from ..service.logging   import logger, clog


# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def nixos(): pass

@nixos.command()
@click.option('--yes'
             , type=bool
             , is_flag=True
             , help='Yes for everything.')
@clog.simple_verbosity_option(logger)
def nixos():
  """Set up a NixOS environment for Agda"""
  MSG = "Agda-pkg will copy the following files to the current directory."
  click.echo(MSG)
  for file in SUPPORT_FILES_PATH.iterdir():
    print(file.as_posix())
  if click.confirm('Do you want to proceed?'):
    pwd = Path().cwd()
    copy_tree(SUPPORT_FILES_PATH.as_posix(), pwd.as_posix(), update=1, verbose=1)
