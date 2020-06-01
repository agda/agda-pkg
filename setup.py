'''
  apkg
  ~~~~

  A package manager for Agda.

'''

# ----------------------------------------------------------------------------

from __future__  import absolute_import, print_function


import io
import os
import re

from os.path     import basename, dirname, join
from setuptools  import find_packages, setup

from apkg.__version__  import __version__

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
  , url='https://github.com/agda/agda-pkg'
  , license='MIT'
  , author='Jonathan Prieto-Cubides and https://github.com/agda/agda-pkg/graphs/contributors'
  , author_email='jonathan.cubides@uib.no'
  , description='A package manager for Agda'
  , long_description='%s' % (read('README.md'))
  , long_description_content_type='text/markdown'
  , packages=find_packages()
  , zip_safe=False
  , include_package_data=True
  , package_dir={'apkg': 'apkg'}
  , package_data={'apkg': ['commands/templates/*', 'support/nixos/*']}
  , platforms='any'
  , keywords=
    [ 'agda'
    , 'package-manager'
    , 'agda-pkg'
    , 'apkg'
    ]
  , install_requires=
    [ 'click'
    , 'gitpython'
    , 'pony'
    , 'whoosh'
    , 'ponywhoosh'
    , 'natsort'
    , 'click-log'
    , 'requests'
    , 'humanize'
    , 'Jinja2'
    , 'distlib'
    , 'PyYAML>=5.1.1'
    ]
  , entry_points='''
      [console_scripts]
      agda-pkg=apkg.apkg:cli
      apkg=apkg.apkg:cli
      '''
  , classifiers=
    [ 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python :: 3.6'
    ]
)
