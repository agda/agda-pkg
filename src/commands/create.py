'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click
import shutil
import yaml
import os
import uuid


from pathlib             import Path
from distutils.dir_util  import copy_tree, remove_tree
from jinja2              import Environment, FileSystemLoader

from ..config            import ( AGDA_PKG_PATH, AGDA_DIR_PATH, AGDA_VERSION 
                                , LIB_SUFFIX, PKG_SUFFIX
                                )
from ..service.logging   import logger, clog


basedir = os.path.dirname(os.path.realpath(__file__))

# ----------------------------------------------------------------------------

# -- Command def.
@click.group()
def create(): pass

@create.command()
@click.option('--yes'
             , type=bool
             , is_flag=True 
             , help='Yes for everything.')
@clog.simple_verbosity_option(logger)
def create(yes):
  """Help to create an Agda Library from a skeleton."""

  # name = "lib"
  # depend = ["sta1", "sta2"]
  # include = ["src", "src2", "src3"]
  # authors = ["Jonathan", "NadieMas"]
  # version = "v2123"
  # homepage = "http:////////"
  # license = "MIIIIIT"
  # sourceRepository = "htgithub..."
  # description = "joderjoder"
  # categories = ["cat1", "cat2"]
  # testedWith = ["2.5.4", "2.5.4"]

  name = click.prompt('Library name'
              , default="test"
              , type=str)

  include = set()
  if click.confirm('Do you want to add a include path?'):
    include.add(click.prompt('PATH', default="src", type=str))
    while click.confirm('Another include?'):
      include.add(click.prompt('PATH', type=str))

  depend = set()
  if click.confirm('Do you want to add a dependency (Library name)?'):
    depend.add(click.prompt('Dependency name', default="standard-library", type=str))
    while click.confirm('Another dependency?'):
      depend.add(click.prompt('Dependency name', type=str))

  moreInfo = click.confirm(
    "Do you want add other information?\n"+
    "This will create an Agda-Pkg file (.agda-pkg) more verbose.")

  if moreInfo:
    version = click.prompt('version (format: vX.X.X)', default="v0.0.1", type=str)

    description = click.prompt('Library description'
                      , default= name + " is an Agda library ..."
                      , type=str)

    categories = set()
    if click.confirm('Do you want to add a category or keyword?'):
      categories.add(click.prompt('category/keyword', type=str))
      while click.confirm('Another category or keyword?'):
        categories.add(click.prompt('category/keyword', type=str))

    authors = set()
    if click.confirm('Do you want add an author?'):
      authors.add(click.prompt('Author name', type=str))
      if click.confirm('Another author?'):
        authors.add(click.prompt('Author name', type=str))

    homepage = click.prompt('Homepage/website', default="None", type=str)
    license = click.prompt('license', default="MIT", type=str)
    sourceRepository = click.prompt('source repository (e.g., http://github.com/pepito/'+name, default="", type=str)

    testedWith = set()
    testedWith.add( click.prompt('Tested with Agda version (X.X.X)', default=AGDA_VERSION, type=str) )
    while click.confirm('Add another Agda version?'):
      testedWith.add( click.prompt('Agda version', type=str) )

  
  pwd = Path().cwd()
  libPath = pwd.joinpath(name)
  if libPath.exists():
    if yes or click.confirm("Delete the directory ("+ name + ") to proceed?", abort=True):
      remove_tree(libPath.as_posix())
    else:
      newDirName = name+"-"+str(uuid.uuid1())
      click.info("Saving on ({})".format(newDirName))
      libPath = pwd.joinpath(newDirName)

  templates = Path(basedir).joinpath('templates')

  libPath.mkdir()
  libPath.joinpath("README.md").touch()
  libPath.joinpath("LICENSE.md").touch()
  
  libPath.joinpath(".gitignore")\
         .write_text(templates.joinpath("gitignore.template").read_text())

  for dir in include:
    libPath.joinpath(dir).mkdir()

  
  env = Environment( loader=FileSystemLoader(templates.as_posix())
                    , trim_blocks=False
                    , lstrip_blocks=False)

  libFile   = env.get_template('library.agda-lib')
  pkgFile   = env.get_template('library.agda-pkg')


  output = libFile.render(name=name, depend=depend, include=include)

  fileName = libPath.joinpath(name + LIB_SUFFIX)
  with open(fileName.as_posix(), 'w') as f:
      f.write(output)

  output = pkgFile.render( name=name
                         , depend=list(depend)
                         , include=list(include)
                         , authors=list(authors)
                         , version=version
                         , homepage=homepage
                         , license=license
                         , sourceRepository=sourceRepository
                         , description=description
                         , categories=list(categories)
                         , testedWith=list(testedWith)
                         )

  fileName = libPath.joinpath(name + PKG_SUFFIX)
  with open(fileName.as_posix(), 'w') as f:
      f.write(output)

    # pkgFile = env.get_template('library.agda-pkg')



  


