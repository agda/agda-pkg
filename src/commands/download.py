'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
from tempfile import *

# ----------------------------------------------------------------------------


def download(index=True):
  pass


@click.group()
def download():
  pass

@download.command()
@click.argument('name')
@click.option('--output-path', '-op')
def download(name, output_path):
  click.echo("No supported at the moment")
  # click.echo('%s' % name)
  # click.echo('%s' % output_path)
  # tempdir = TemporaryDirectory()
  # print(tempdir)
