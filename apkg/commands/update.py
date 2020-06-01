'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click


from pony.orm  import db_session, select

from .install            import install
from .uninstall          import uninstall
from ..service.database  import db
from ..service.database  import ( Library )
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

@click.group()
def update():
	pass

@update.command()
@click.argument('libnames', nargs=-1)
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def update(ctx, libnames):
  """Update packages to latest indexed version."""

  logger.info("Updating.")
  wasUpdated = False
  if len(libnames) == 0:
    libraries = select(l.name for l in Library if l.installed)[:]
  else:
    libraries = libnames

  for lname in libraries:
    library = Library.get(name = lname)
    installedVersion = library.getInstalledVersion()
    latestVersion    = library.getLatestVersion()
    if installedVersion is not latestVersion:
      try:
        ctx.invoke(uninstall, libname=lname, yes=True)
        ctx.invoke(install, libnames=[lname], version=latestVersion.name, yes=True)
        wasUpdated = True
      except Exception as e:
        logger.error(e)
          
  if wasUpdated:
    logger.info("Libraries updated.")
  else:
    logger.info("Everything is up-to-date.")
