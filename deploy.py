from pathlib import Path
import click
import subprocess

from src.__version__ import __version__, __message__


print("Version: v" + __version__)
print("Message: " + __message__)

if click.confirm("Proceed"):
  subprocess.run(["git", "add" , "."], stdout=subprocess.PIPE)
  subprocess.run(["git", "commit" , "-am", "[ v{} ] {}".format(__version__, __message__)]
                , stdout=subprocess.PIPE)
  subprocess.run(["make", "pip-package"], stdout=subprocess.PIPE)
  subprocess.run(["git", "push" , "origin", " master", "--tags"], stdout=subprocess.PIPE)