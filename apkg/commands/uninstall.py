'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click

from pathlib    import Path
from pony.orm   import db_session, commit

from ..config   import ( AGDA_DEFAULTS_PATH
                       , AGDA_DIR_PATH
                       , AGDA_LIBRARIES_PATH
                       , AGDA_PKG_PATH
                       , AGDA_VERSION
                       , DATABASE_FILE_NAME
                       , DATABASE_FILE_PATH
                       , DATABASE_SEARCH_INDEXES_PATH
                       , GITHUB_USER
                       , INDEX_REPOSITORY_BRANCH
                       , INDEX_REPOSITORY_NAME
                       , INDEX_REPOSITORY_PATH
                       , INDEX_REPOSITORY_URL
                       , REPO
                       , LIB_SUFFIX
                       , PKG_SUFFIX
                       )

from .write_defaults              import write_defaults
from ..service.readLibFile        import readLibFile
from ..service.database           import db, pw
from ..service.database           import ( Library
                                         , LibraryVersion
                                         , Keyword
                                         , TestedWith
                                         , Dependency
                                         )
from ..service.logging            import logger, clog


# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def uninstall():
  pass

@db_session
def uninstallLibrary(libname, database=False, remove_cache=False):
  library = Library.get(name = libname)
  if library is None \
    or (not library.installed and not (remove_cache)): 
    logger.info("This library is not installed.")
    return False
  
  try:
    if database:
      library.delete()
    else:
      if library.installed:
        library.uninstall(remove_cache)
        logger.info("Removed {} from the agda-pkg database.".format(libname))
    commit()
    return True
  
  except Exception as e:
    logger.error(e)
    logger.error(" Unsuccessfully call.")
  return False

@uninstall.command()
@click.argument('libname')
@click.option('--database'
             , type=bool
             , default=False
             , is_flag=True 
             , help='Remove a package from the agda-pkg database')
@click.option('--remove-cache'
             , type=bool
             , default=False
             , is_flag=True 
             , help='Remove all package files.')
@clog.simple_verbosity_option(logger)
@click.option('--yes'
             , type=bool
             , is_flag=True 
             , help='Yes for everything.')
@click.pass_context
@click.confirmation_option(prompt='Proceed?')
@db_session
def uninstall(ctx, libname, database, remove_cache,yes):
  """Uninstall a package."""

  if libname == "." :
    pwd = Path().cwd()

    if not Path(pwd).exists():
      logger.error(pwd + " doesn't exist!")
      return None
    
    agdaLibFiles = [ f for f in pwd.glob("*" + LIB_SUFFIX) if f.is_file() ]
    agdaPkgFiles = [ f for f in pwd.glob("*" + PKG_SUFFIX) if f.is_file() ]

    if len(agdaLibFiles) == 0 and len(agdaPkgFiles) == 0:
      logger.error("No libraries (" + LIB_SUFFIX + " or "\
                  + PKG_SUFFIX + ") files detected." )
      return None

    libFile = Path("")
    
    # -- TODO: offer the posibility to create a file agda-pkg!
    if len(agdaPkgFiles) == 1:
      libFile = agdaPkgFiles[0]
    elif len(agdaLibFiles) == 1:
      # -- TODO: offer the posibility ssto create a file agda-pkg!
      libFile = agdaLibFiles[0]
    else:
      logger.error("None or many agda libraries files.")
      logger.info("[!] Use --name to specify the library name.")
      return None

    logger.info("Library file detected: " + libFile.name)
    info = readLibFile(libFile)

    libname = info.get("name", "")

  if libname == "." or libname == "":
    logger.error(" we could not know the name of the library to uninstall.")
    return

  if uninstallLibrary(libname, database, remove_cache):
    ctx.invoke(write_defaults, yes = yes)