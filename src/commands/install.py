import click
from gitapkg import GitApkg

@click.group()
def install():
  click.echo('[Clone]: initializing cloning')
  GitApkg().clone()
  click.echo('[Clone]: repository successfully cloned')

@install.command()
def local():
  click.echo('This is the zone subcommand of the install command')
