'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click


from git       import *
from pony.orm  import *

from distlib.index  import PackageIndex
from natsort        import natsorted

from .__version__   import __version__

# ----------------------------------------------------------------------------


try:
  index    = PackageIndex()
  info     = index.search('agda-pkg')
  versions = natsorted([e["version"] for e in info if e["name"] == "agda-pkg"])


  if len(versions) > 0:
    lastversion = versions[-1]
    msg = "Your Agda-Pkg version is {cversion}, however version {lversion} is available.\n" + \
          "Consider upgrading via 'pip install --upgrade agda-pkg'."
    msg = msg.format(cversion = __version__ , lversion = lastversion)
    orden = [lastversion, __version__]
    if orden != natsorted(orden):
      click.echo(click.style(msg, fg='yellow', bold=True))

  # Check if the index is updated.

  from .config           import REPO
  origin = REPO.remotes["origin"]
  repo   = REPO.git
  origin.fetch()
  status = repo.status()
  if "is behind" in status:
    packageURL = [url for url in REPO.remote().urls][0]
    msg = "Your package-index database is outdated with:\n" + \
          "  " + packageURL + "\n" +\
          "Consider upgrading it by running the command:\n" +\
          "  $ apkg upgrade\n"

    click.echo(click.style(msg, fg='yellow', bold=True))
except:
  pass


