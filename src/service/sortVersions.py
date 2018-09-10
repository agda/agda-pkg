'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pony.orm import *

from natsort import natsorted
from operator import attrgetter, itemgetter

@db_session
def sortVersions(libname):
  lib = Library.get(name = libname)
  if lib is None: return []
  versions = [v for v in lib.versions]
  sortedVersions = natsorted(versions, key=attrgetter('name'))
  return sortedVersions
