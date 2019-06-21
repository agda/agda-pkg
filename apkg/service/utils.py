'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

from pathlib             import Path
from pony.orm            import *
from urllib.parse        import urlparse

from ..service.database  import db
from ..service.database  import ( Library
                                , LibraryVersion
                                )

# ----------------------------------------------------------------------------

# -- Some tests -- TODO: move these to some util module outside.
def isURL(url):
  min_attr = ('scheme' , 'netloc')
  try:
    result = urlparse(url)
    # -- TODO : improve this test checking if it's available
    return all([result.scheme, result.netloc])
  except:
    return False

def isGit(url):
  min_attr = ('scheme' , 'netloc')
  try:
    result = urlparse(url)
    netloc = result.netloc
    # -- TODO : improve this test using gitpython
    return all([result.scheme, result.netloc]) and result.path.endswith(".git")
  except:
    return False

@db_session
def isIndexed(libname):
  return Library.get(name=libname) is not None

def isLocal(path):
  return Path(path).exists()
