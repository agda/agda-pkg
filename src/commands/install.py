import click


@click.group()
def install():
  pass

@install.command()
def local():
  click.echo('This is the zone subcommand of the install command')
