'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

# ----------------------------------------------------------------------------

@click.group()
def update():
	pass

@update.command()
@click.argument('name')
@click.option('--package', '-p', type=float, default=-1.0)
def update(name, package):
  click.echo('%s' % name)
  click.echo(package)