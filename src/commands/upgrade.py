'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

from git       import *
from pony.orm  import *

from .init     import init
from ..config  import REPO

# ----------------------------------------------------------------------------

@click.group()
def upgrade(): pass

class ProgressPrinter(RemoteProgress):
  def update(self, op_code, cur_count, max_count=None, message=''):
    print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

@upgrade.command()
@click.pass_context
def upgrade(ctx):
  """Update the list of available packages."""
  origin = REPO.remotes["origin"]
  click.echo("Updating Agda-Pkg from " + [url for url in REPO.remote().urls][0])
  for pull_info in origin.pull(progress=ProgressPrinter()):
    click.echo("%s to %s" % (pull_info.ref, pull_info.commit))
  ctx.invoke(init, drop_tables=False)
  


