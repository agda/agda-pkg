'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from pathlib import *

from ..config import ( AGDA_DEFAULTS_PATH
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
                     )

from ..service.readLibFile import readLibFile
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pprint   import pprint
from pony.orm import *
from ponywhoosh  import PonyWhoosh, search, full_search

@click.group()
def search():
  pass


@search.command()
@click.argument('term')
@click.option('--field', '-f', type=str, default=None)
def search(term, field):
  """Search into the package index."""
  results = \
    pw.search(
        term
      , models = ["Library", "Keyword"]
      , fields = (field if field is not None else ["name", "url", "description", "word"])
      , include_entity = True
      , something = True
      )
  libraries = results["results"].get('Library', {'items':[]})['items']

  click.echo( str(len(libraries)) + " result" +("s" if len(libraries) != 1 else "") +  " in " + str(results['runtime']) + "seg")
  if len(libraries) > 0:
    click.echo( "matches: " + str(results['matched_terms']))
    click.echo("")

    for result in libraries:
      click.echo(result["entity"]["name"])
      click.echo("="*len(result["entity"]["name"]))
      del result["entity"]["name"]
      for k, v in result["entity"].items():
        if  v != None:
          click.echo("{0}: {1}".format(k,v))
      click.echo("")
