import click


@click.group()
def upgrade():
	pass

@upgrade.command()
@click.option('--package-name', '-pn')
def upgrade(package_name):
  click.echo('%s' % package_name)
