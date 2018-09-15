'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------

import click

from ..service.readLibFile import readLibFile
from ..service.database    import db, pw
from ..service.database    import ( Library
                                  , LibraryVersion
                                  , Keyword
                                  , TestedWith
                                  , Dependency
                                  )
from ..service.sortVersions import sortVersions
from pprint   import pprint
from pony.orm import *

import logging
import click_log as clog
# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def info():
    pass

@info.command()
@click.argument('libname')
@click.option('--version', type=str, default="", help='info of one version')
@click.option('--field', type=str, default="", help='info of one field')
@clog.simple_verbosity_option(logger)
@db_session
def info(libname, version, field):
  """Show information about one package"""
  if version == "":
    logger.info("There's no version nunmber")
    lib = Library.get(name = libname)

    if lib is None:
      logger.info(libname + " is not in the index")
      print("No available")
      return

    versions = sortVersions(lib.name)
    if len(versions) == 0:
      logger.error("Database is corrupted. This library has no versions available")
      logger.info("Repair the database by running: apkg init")
      return

    lastversion = versions[0]

    try:
      info = readLibFile(lastversion.info_path)
      logger.info("Read" + lastversion.info_path)
    except Exception as e:
      logger.error(e)

    if field != "":
      if field in info:
        click.echo(info[field])
      else:
        click.echo("No information about " + field)
    else:
      for k, v in info.items():
        if k is "version": pass
        if (type(v) == str or type(v) == list) and len(v) > 0:
          click.echo("{0}: {1}".format(k, v))

    if len(versions) > 0:
      click.echo("Versions available:")
      for v in versions:
        ms = "  - %s" % v.name \
          + (" ==> Latest!" if v.latest else "") \
          + (" ==> Installed!" if v.installed else "")
        click.echo(ms)
