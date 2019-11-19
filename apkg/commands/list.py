'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
import logging
import click_log as clog

from operator            import attrgetter, itemgetter
from pony.orm            import db_session, select
from natsort             import natsorted

from ..service.database  import db
from ..service.database  import ( Library , LibraryVersion )
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def list(): pass


listFields = ["name", "version", "url"]


@list.command()
@clog.simple_verbosity_option(logger)
@click.option('--full'
             , type=bool
             , is_flag=True 
             , help='Show name, version and description per package.'
             )
@click.option('--field'
             , type=str
             , default=""
             , help='Show a specific field e.g.: name, version, url')
@db_session
def list(full, field):
  """List all installed packages."""

  short = not full 

  libraries = select(l for l in Library if l)[:]
  libraries = natsorted(libraries, key=lambda x : attrgetter('name')(x).lower())

  if len(libraries) == 0:
    logger.info("[!] No libraries available to list.")  
    logger.info("    Consider run the following command:")
    logger.info("      $ apkg init")
    return 



  orderFields = [  
                #, "library"
                #, "sha"
                  "description"
                # , "license"
                # , "include"
                # , "depend"
                # , "testedWith"
                , "keywords"
                # , "installed"
                # , "cached"
                # , "fromIndex"
                # , "fromUrl"
                # , "fromGit"
                , "origin"
                # , "default"
                ]

  i  = 0
  if short and field == "":
    logger.info("{:<20.20} {:<15.20} {:.72}"
                    .format("Library name", "Latest version", "URL"))
    logger.info("-"*105)

  for library in libraries:
    v = library.getLatestVersion()    
    if v is not None:
      if not short:

        logger.info(v.library.name)
        logger.info("="*len(v.library.name))

        info = v.info

        for k in orderFields: 
          val = info.get(k, None)
          if val is not None or val != "" or len(val) > 0:
            click.echo("{0}: {1}".format(k,val))

        vs = ','.join(str(ver) for ver in v.library.versions)
       
        if len(vs) > 0:
          print("Versions:", vs)
      
      else:
        if field in listFields:
          if field == "name":
            print(v.library.name)
          elif field == "version":
            print(v.name)
          else:
            print(v.library.url)
        else:
          print("{:<20.20} {:<15.20} {:.72}"
                .format(v.library.name,v.name,v.library.url))

      i += 1
      if not short and i < len(libraries):
        logger.info("")