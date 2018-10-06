'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
import shutil

from pathlib             import Path
from distutils.dir_util  import copy_tree, remove_tree

from ..config            import AGDA_PKG_PATH,AGDA_DIR_PATH, AGDA_VERSION 
from ..service.logging   import logger, clog

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def create(): pass

@create.command()
@clog.simple_verbosity_option(logger)
def create():
  """Created a skeleton of a library."""


  name = click.prompt('Library name'
              , default="test"
              , type=str)

  # include = set()
  # if click.confirm('Do you want to add a include path (source)?'):
  #   include.add(click.prompt('PATH:', default="src", type=str))
  #   while click.confirm('Another include?'):
  #     include.add(click.prompt('PATH:', type=str))

  # depend = set()
  # if click.confirm('Do you want to add a dependency (Library name)?'):
  #   depend.add(click.prompt('Dependency name:', type=str))
  #   while click.confirm('Another dependency?'):
  #     depend.add(click.prompt('Dependency name:', type=str))

  # moreInfo = click.confirm(
  #   "Do you want add other information?\n"+
  #   "This will create an Agda-Pkg file (.agda-pkg) more verbose.")

  # if moreInfo:
  #   version = click.prompt('version (format: vX.X.X)', default="v0.0.1", type=str)

  #   description = click.prompt('Library description'
  #                     , default= name " is an Agda library ..."
  #                     , type=str)

  #   categories = set()
  #   if click.confirm('Do you want to add a category or keyword?'):
  #     categories.add(click.prompt('category/keyword', type=str))
  #     while click.confirm('Another category or keyword?'):
  #       categories.add(click.prompt('category/keyword', type=str))

  #   authors = set()
  #   if click.confirm('Do you want add an author?'):
  #     authors.add(click.prompt('Author name', type=str))
  #     if click.confirm('Another author?'):
  #       authors.add(click.prompt('Author name', type=str))

  #   homepage = click.prompt('Homepage/website', default="None", type=str)
  #   license = click.prompt('license', default="MIT", type=str)
  #   sourceRepository = click.prompt('source repository (e.g., http://github.com/pepito/'+name, default="", type=str)

  #   testedWith = set()
  #   testedWith.add( click.prompt('Tested with Agda version (X.X.X)', default=AGDA_VERSION, type=str) )
  #   while click.confirm('Add another Agda version?'):
  #     testedWith.add( click.prompt('Agda version', type=str) )

  # ## agda.lib
  
  pwd = Path().cwd()
  libPath = pwd.joinpath(name)
  if libPath.exists():
    if click.confirm("Delete the directory "+ name + " to proceed?", abort=True):
      remove_tree(libPath.as_posix())
    libPath.mkdir()
    libPath.joinpath("README.md").touch()
    libPath.joinpath("LICENSE.md").touch()
    libPath.joinpath(".gitignore").touch()
    
    for dir in include:
      libpath.joinpath(dir).mkdir()



  # if moreinfo:
  # ##


  


