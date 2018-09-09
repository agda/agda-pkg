'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click
from tempfile import *

@click.group()
def download():
  pass

@download.command()
@click.argument('name')
@click.option('--output-path', '-op')
def download(name, output_path):
  click.echo('%s' % name)
  click.echo('%s' % output_path)
  tempdir = TemporaryDirectory()
  print(tempdir)
