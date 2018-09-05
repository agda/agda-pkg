'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click


@click.group()
def info():
    pass

@info.command()
@click.argument('name')
def info(name):
  click.echo('%s' % name)
