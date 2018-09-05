'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from git      import *

from ..config import init_files

@click.group()
def init():
	pass

@init.command()
def init():
  init_files()



