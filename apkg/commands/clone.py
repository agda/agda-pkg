'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

import click
import logging
import click_log
import requests
import humanize

from pony.orm            import db_session, select
from distutils.dir_util  import copy_tree, remove_tree
from pathlib             import Path

from ..config            import ( PACKAGE_SOURCES_PATH
                                , INDEX_REPOSITORY_PATH
                                , PKG_SUFFIX
                                , GITHUB_DOMAIN
                                , LIB_SUFFIX
                                , GITHUB_API
                                )

from ..service.database  import db
from ..service.database  import ( Library , LibraryVersion )
from ..service.logging   import logger, clog
from ..service.utils     import isURL, isGit, isIndexed, isLocal

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def clone(): pass

@clone.command()
@click.argument('urladdress', nargs=-1)
@click.option('--outdir'
             , type=str
             , default='.'
             , help='Output directory.')
@click.option('--version'
             , type=str
             , help='Version, tag or commit.')
@click.option('--url'
             , type=bool
             , is_flag=True
             , help='From a url address.')
@click.option('--git'
             , type=bool
             , is_flag=True
             , help='From a git repository.')
@click.option('--github'
             , type=bool
             , is_flag=True
             , help='From a github repository.')
@click.option('--branch'
             , type=str
             , default="master"
             , help='From a git repository.')
@click.option('--yes'
             , type=bool
             , is_flag=True
             , help='Yes for everything.')
@clog.simple_verbosity_option(logger)
@click.pass_context
@db_session
def clone(ctx, urladdress, outdir, version, url, git, github, branch, yes):
  """Clone the Adga library as with git clone"""
  if len(urladdress) == 0:
    logger.error(" Specify the url of the repository or the library name from the package index.")
    return

  if isGit(urladdress): url = True

  logger.info("Clonning: %s" % urladdress )

  if len(outdir) == 0 or outdir == ".":
    outputdir = Path().cwd()
  else:
    outputdir = Path(outdir)

  try:
    click.echo("Using directory: {}".format(outputdir))

    if Path(outputdir).exists() and click.confirm('Do you want to overwrite the library files'):
      remove_tree(outputdir)

    # To display a nice progress bar, we need the size of
    # the repository, so let's try to get that number

    # -- SIZE Repo

    size = 0
    if "github" in urladdress:

      reporef = urladdress.split("github.com")[-1]
      infourl = GITHUB_API + reporef.split(".git")[0]

      response = requests.get(infourl, stream=True)

      if not response.ok:
        logger.error("Request failed: %d" % response.status_code)
        return None

      info = response.json()
      size = int(info.get("size", 0))

    else:

      response = requests.get(url, stream=True)
      if not response.ok:
        logger.error("Request failed: %d" % response.status_code)
        return None

      size_length = response.headers.get('content-length')
      size = 0
      if size_length is None:
        for _ in response.iter_content(1024):
            size += 1024
      else:
        size = size_length
      size = int(size)

    logger.info("Downloading " + urladdress \
          + " (%s)" % str(humanize.naturalsize(size, binary=True)))

    with click.progressbar( length=10*size
                          , bar_template='|%(bar)s| %(info)s %(label)s'
                          , fill_char=click.style('█', fg='cyan')
                          , empty_char=' '
                          , width=75
                          ) as bar:

      class Progress(git.remote.RemoteProgress):

        total, past = 0 , 0

        def update(self, op_code, cur_count, max_count=None, message=''):

          if cur_count < 10:
            self.past = self.total
          self.total = self.past + int(cur_count)

          bar.update(self.total)

      click.echo("Git branch: " + branch)

      REPO = git.Repo.clone_from( urladdress
                                , outputdir
                                , branch=branch
                                , progress=Progress()
                                )
    if version != "":
      try:
        # Seen on https://goo.gl/JVs8jJ
        REPO.git.checkout(version)

      except Exception as e:
        logger.error(e)
        logger.error(" version or tag not found ({})".format(version))

  except Exception as e:
    logger.errorr(e)