'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

from distlib.index  import PackageIndex
from natsort        import natsorted

from .__version__   import __version__

# ----------------------------------------------------------------------------

index    = PackageIndex()
info     = index.search('agda-pkg')
versions = natsorted([e["version"] for e in info if e["name"] == "agda-pkg"])


if len(versions) > 0:
  lastversion = versions[-1]
  msg = "You are using agda-pkg version {cversion}, however version {lversion} is available.\n" + \
        "You should consider upgrading via the 'pip install --upgrade agda-pkg' command."
  msg = msg.format(cversion = __version__ , lversion = lastversion)
  orden = [lastversion, __version__]
  if orden != natsorted(orden):
    click.echo(click.style(msg, fg='yellow', bold=True))



