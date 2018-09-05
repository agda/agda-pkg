'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click


@click.group()
def show():
    pass

@show.command()
def show():
  click.echo('This is the zone subcommand of the install command')
