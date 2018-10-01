'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
import logging
import click_log as clog

from pathlib            import Path
from pony.orm           import *

from ..config           import ( PACKAGE_SOURCES_PATH
                               , INDEX_REPOSITORY_PATH
                               , INDEX_REPOSITORY_URL
                               )

from ..service.database import db
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )

# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def init():	pass

@init.command()
@clog.simple_verbosity_option(logger)
@click.option('--drop_tables', type=bool, default=True)
def init(drop_tables):
  """Initialize Agda-Pkg state."""

  if drop_tables:
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

  f = INDEX_REPOSITORY_PATH
  src = f.joinpath("src")
  click.echo("Indexing libraries from " + INDEX_REPOSITORY_URL)

  with db_session:

    for lib in src.glob("*"):
      name = lib.name
      url  = Path(lib).joinpath("url").read_text()
      library = Library.get(name = name, url = url)
      if library is None:
        library = Library(name = name, url = url)

      for version in lib.joinpath("versions").glob("*"):
        if version.is_dir():
          libVersion = LibraryVersion.get( library=library
                                         , name=version.name
                                         , fromIndex=True
                                         )
          if libVersion is None:
            libVersion = LibraryVersion( library=library
                                       , name=version.name
                                       , fromIndex=True
                                       )

          if version.joinpath("sha1").exists():
            libVersion.sha = version.joinpath("sha1").read_text()
            libVersion.origin  = url
            libVersion.fromGit = True
          else:
            logger.error(version.name + " no valid")
            libVersion.delete()

        commit()

    # With all libraries indexed, we proceed to create the dependencies
    # as objects for the index.
    for lib in src.glob("*"):
      library = Library.get(name = lib.name)

      for version in library.getSortedVersions():
        # click.echo(version.freezeName)

        info = version.readInfoFromLibFile()

        version.depend.clear()
        for depend in info.get("depend", []):
          if type(depend) == list:
            logger.info("no supported yet but the format is X.X <= name <= Y.Y")
          else:
            dependency = Library.get(name = depend)
            if dependency is not None:
              version.depend.add(Dependency(library = dependency))
            else:
              logger.warning(depend + " is not in the index")

        info = version.readInfoFromLibFile()

        keywords = info.get("keywords", []) + info.get("category", [])
        keywords = list(set(keywords))

        for word in keywords:
          keyword =  Keyword.get(word = word)
          if keyword is None:
            keyword = Keyword(word = word)

          keyword.libraries.clear()
          keyword.libraries.add(library)

          keyword.libVersions.clear()
          keyword.libVersions.add(version)


    libraries = select(l for l in Library)[:]

    click.echo( str(len(libraries)) + " librar" \
        + ("ies" if len(libraries) != 1 else "y")  \
        + " indexed."
        )

    logger.info("")
    logger.info("[+] Check all the available libraries by running")
    logger.info("    the command:")
    logger.info("    $ apkg list")