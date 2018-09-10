'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

@click.group()
def install():
  click.echo('[Clone]: initializing cloning')
  click.echo('[Clone]: repository successfully cloned')

# @install.command()
# def install():
#   click.echo('This is the zone subcommand of the install command')

@install.command()
def local():
  click.echo('This is the zone subcommand of the install command')
