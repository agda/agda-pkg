'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
import click
from pathlib import Path

from ..config import PACKAGE_SOURCES_PATH, INDEX_REPOSITORY_PATH

from ..service.readLibFile  import readLibFile
from ..service.sortVersions import sortVersions
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )
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
def init():	pass

@init.command()
@clog.simple_verbosity_option(logger)
def init():
  db.drop_all_tables(with_all_data=True)
  db.create_tables()

  f = INDEX_REPOSITORY_PATH
  src = f.joinpath("src")

  logger.info("Indexing packages...")
  with db_session:
    for lib in src.glob("*"):
      name = lib.name
      url  = Path(lib).joinpath("url").read_text()
      library = Library(name = name)
      library.url = url
      library.localpath = lib.as_posix()

      for version in lib.joinpath("versions").glob("*"):
        libVersion = LibraryVersion( library = library , name = version.name)
        locationName = name + ("@" + version.name if len(version.name) > 0 else "")
        libVersion.installation_path = PACKAGE_SOURCES_PATH.joinpath(locationName).as_posix()

        if version.joinpath("sha1").exists():
          libVersion.sha = version.joinpath("sha1").read_text()
        else:
          logger.info("ERROR: "+ version.name + " no valid")

        agdaLibFile = version.joinpath(name + ".agda-lib")
        agdaPkgFile = version.joinpath(name + ".agda-pkg")

        if agdaLibFile.exists():
          libVersion.info_path = agdaLibFile.as_posix()
        if agdaPkgFile.exists():
          libVersion.info_path = agdaPkgFile.as_posix()

    # With all libraries indexed, we proceed to create the dependencies
    # as objects for the index.

    for lib in src.glob("*"):
      library = Library.get(name = lib.name)
      versions = sortVersions(lib.name)
      if len(versions) > 0:
        versions[-1].latest = True

      logger.info("\n" +  name)
      logger.info("="*len(name))
      logger.info("- URL: %s" % url + "- Versions:")

      for version in versions:
        logger.info( "  * v" + version.name + (" Latest" if version.latest else ""))
        info = readLibFile(version.info_path)
        keywords = info.get("keywords", [])
        if keywords == []:
          keywords = info.get("category", [])

        for word in keywords:
          keyword =  Keyword.get(word = word)
          if keyword is None:
            keyword = Keyword(word = word)
          keyword.libraries.add(library)
          keyword.libversions.add(version)

        for depend in info["depend"]:
          if type(depend) == list:
            logger.info("no supported yet but the format is X.X <= name <= Y.Y")
          else:
            dependency = Library.get(name = depend)
            if dependency is not None:
              version.requires.add(Dependency(library = dependency))
            else:
              logger.warning(depend + " is not in the index")
    commit()
