'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from git      import *

from ..config import setup

@click.group()
def init():
	pass

@init.command()
def init():
  setup()