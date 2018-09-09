'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import click

from git      import *
from ..config import *

@click.group()
def upgrade():
	pass

class ProgressPrinter(RemoteProgress):
  def update(self, op_code, cur_count, max_count=None, message=''):
    print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

# This update the index
@upgrade.command()
def upgrade():
  REPO = setup()
  origin = REPO.remotes["origin"]
  click.echo("Updating index from " + [url for url in REPO.remote().urls][0])
  for pull_info in origin.pull(progress=ProgressPrinter()):
    click.echo("%s to %s" % (pull_info.ref, pull_info.commit))
  # after this, we should update the database...
