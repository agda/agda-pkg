from ..service.writeAgdaDirFiles import writeAgdaDirFiles
from pony.orm import *
import click
from ..service.sortVersions import sortVersions
from ..service.database import ( Library )

try:
  with db_session:
    libraries = select(library for library in Library)[:]
    for library in libraries:
      versions = sortVersions(library.name)
      if len(versions) > 0:
        versions[-1].latest = True
except Exception as e:
  click.echo(str(e))

writeAgdaDirFiles()
