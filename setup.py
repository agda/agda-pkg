'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

from __future__  import absolute_import, print_function


import io
import os
import re

from os.path     import basename, dirname, join
from setuptools  import find_packages, setup

from src.__version__  import __version__

# ----------------------------------------------------------------------------

def read(*names, **kwargs):
  return io.open(
      join(dirname(__file__), *names)
    , encoding=kwargs.get('encoding', 'utf8')
  ).read()


setup(
    name='agda-pkg'
  , version=__version__
  , python_requires='>=3.6.0'
  , url='https://github.com/apkgbot/agda-pkg'
  , license='MIT'
  , author='Jonathan Prieto-Cubides'
  , author_email='jcu043@uib.no'
  , description='The Agda Package Manager'
  , long_description='%s' % (read('README.md'))
  , long_description_content_type='text/markdown'
  , packages=find_packages()
  , zip_safe=False
  , include_package_data=True
  , package_data = {'agda_pkg': ['README.md']}
  , platforms='any'
  , keywords=
    [ 'agda'
    , 'package-manager'
    , 'agda-pkg'
    ]
  , install_requires=
    [ 'click'
    , 'gitpython'
    , 'pyyaml'
    , 'pony'
    , 'whoosh'
    , 'ponywhoosh'
    , 'natsort'
    , 'click-log'
    , 'requests'
    , 'humanize'
    , 'Jinja2'
    , 'distlib'
    ]
  , entry_points='''
      [console_scripts]
      agda-pkg=src.apkg:cli
      apkg=src.apkg:cli
      '''
  , classifiers=
    [ 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python :: 3.6'
    ]
)
