import click
import os, sys

@click.group()
#@click.option('--count', default=1, help='Number of greetings.')
#@click.option('--name', prompt='Your name',
#              help='The person to greet.')
def setup():
    #for x in range(count):
    #    click.echo('Hello %s!' % name)
    pass

@click.command()
def version():
	click.echo('1.0')

@click.command()
def update():
	click.echo('git pull origin master')

@click.command()
def install():
	click.echo('git clone bla')
	sys.stdout.writelines('pwd')
	click.launch('git clone https://github.com/apkgbot/agda-packages.git')

setup.add_command(install)
setup.add_command(update)
setup.add_command(version)

if __name__ == '__main__':
    setup()
