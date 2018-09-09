'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click
import shutil
from pathlib import Path
from ..config import AGDA_PKG_PATH,AGDA_DIR_PATH

@click.group()
def clean():
    pass

@clean.command()
def clean():
  shutil.rmtree(AGDA_PKG_PATH)
  shutil.rmtree(AGDA_DIR_PATH)
