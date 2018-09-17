'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
from ..config import ( AGDA_DEFAULTS_PATH
                     , AGDA_DIR_PATH
                     , AGDA_LIBRARIES_PATH
                     , AGDA_PKG_PATH
                     , AGDA_VERSION
                     , DATABASE_FILE_NAME
                     , DATABASE_FILE_PATH
                     , DATABASE_SEARCH_INDEXES_PATH
                     , GITHUB_USER
                     , INDEX_REPOSITORY_BRANCH
                     , INDEX_REPOSITORY_NAME
                     , INDEX_REPOSITORY_PATH
                     , INDEX_REPOSITORY_URL
                     , PACKAGE_SOURCES_PATH
                     , REPO
                     , PKG_SUFFIX
                     , LIB_SUFFIX
                     )

from pony.orm   import *
from ponywhoosh import PonyWhoosh
from pprint import pprint 

from pathlib import Path
from ..service.readLibFile import readLibFile
from natsort import natsorted
from operator import attrgetter, itemgetter
import yaml

import logging

# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)

# -- Search index
pw = PonyWhoosh()

pw.indexes_path          = DATABASE_SEARCH_INDEXES_PATH
pw.search_string_min_len = 1
pw.writer_timeout        = 3

# -- Database
db = Database()


# Library is the general object to store the information about
# an Agda library. Each library is associated with its different
# versions. These versions are instance of the object LibraryVersion.

@pw.register_model('name', 'description', 'url')
class Library(db.Entity):
    name = PrimaryKey(str)
    description = Optional(str, nullable=True)
    url = Optional(str, nullable=True)
    versions = Set('LibraryVersion')
    appearson = Set('Dependency')
    keywords = Set('Keyword')
    installed = Optional(bool, default=False)
    default = Optional(bool, default=True)

    def __str__(self):
      return self.name

    def __repr__(self):
      return self.name

    @property
    def info(self):
      return self.to_dict( with_collections=True
                         , related_objects=True)

    @property
    def indexPath(self):
      return INDEX_REPOSITORY_PATH.joinpath("src").joinpath(self.name)

    def isIndexed(self):
      return self.indexPath.exist()
      
    def getSortedVersions(self):
      versions = [v for v in self.versions]
      return natsorted(versions, key=attrgetter('name'))

    def getInstalledVersion(self):
      versions = [v for v in self.versions if v.installed]
      if len(versions) == 1: return version[0]
      return None

    def getLatestVersion(self):
      versions = self.getSortedVersions()
      if len(versions) > 0: return versions[-1]
      return None

    def freezeName(self):
      version = self.getInstalledVersion()
      if version is not None:
        return version.locationName()
      return self.name # --not sure about this

@pw.register_model('name', 'description')
class LibraryVersion(db.Entity):
    library = Required(Library)
    name = Optional(str, nullable=True, default="")
    sha = Optional(str)
    description = Optional(str)
    license = Optional(str)
    include = Optional(str, default="src/")
    depend = Set('Dependency')
    testedWith = Set('TestedWith')
    keywords = Set('Keyword')
    installed = Optional(bool, default=False)
    fromIndex = Optional(bool, default=True)
    
    def __str__(self):
      return self.name

    def __repr__(self):
      return self.name

    @property
    def info(self):
      return self.to_dict(with_collections=True
                         , related_objects=True
                         , exclude=["id", "sha"])

    def libraryVersionName(self, sep):
      return self.library.name.strip() + sep + self.name.strip()

    @property
    def locationName(self):
      return self.libraryVersionName("@")

    @property
    def freezeName(self):
      if self.name == "": return self.library.name
      return self.libraryVersionName("==")

    def isIndexed(self):
      return self.fromIndex

    def isUserVersion(self):
      return (not self.isIndexed())

    @property
    def installationPath(self):
      return PACKAGE_SOURCES_PATH.joinpath(self.locationName)

    @property
    def indexPath(self):
      return (INDEX_REPOSITORY_PATH
               .joinpath("src")
               .joinpath(self.library.name)
               .joinpath("versions")
               .joinpath(self.name)
             )

    @property
    def agdaPkgFilePath(self):
      return (self.indexPath.joinpath(self.library.name + PKG_SUFFIX) if (self.isIndexed() and not (self.installed))
              else self.installationPath.joinpath(self.library.name + PKG_SUFFIX))
              
    @property
    def agdaLibFilePath(self):
      return (self.indexPath.joinpath(self.library.name + LIB_SUFFIX) if (self.isIndexed() and not (self.installed))
              else self.installationPath.joinpath(self.library.name + PKG_SUFFIX))
      

    def getLibFilePath(self):
      if self.agdaPkgFilePath.exists():
        return self.agdaPkgFilePath
      if self.agdaLibFilePath.exists():
        return self.agdaLibFilePath
      print(self.agdaPkgFilePath)
      print(self.agdaLibFilePath)
      raise ValueError(" There is not library agda file for this version, is it installed?")

    def isLatest(self):
      versions = self.library.getSortedVersions()
      return len(versions) > 0 and versions[-1].name == self.name

    def tolibFormat(self):
      msg = '\n'.join(
            [ "name: %s" % self.library.name
            , "version: %s" % self.name
            , "include: %s" % ' '.join([inc for inc in self.include.split()])
            , "depend: %s" % ' '.join([dep.library.name for dep in self.depend.split()])
            ])
      return '\n'.join(msg)

    def toPkgFormat(self):
      return yaml.dump(self.info, default_flow_style=False)


    def writeAgdaLibFile(self, path=None):
      if path is None: path = self.agdaLibFilePath()
      path = Path(path)
      if not path.exists(): path.touch()
      path.write_text(self.tolibFormat())

    def writeAgdaPkgFile(self, path=None):
      if path is None: path = self.agdaPkgFilePath()
      path = Path(path)
      if path.exists(): path.touch()
      path.write_text(self.toPkgFormat())

    def writeLibFile(self, path=None,format=PKG_SUFFIX):
      if format == PKG_SUFFIX:
        self.writeAgdaPkgFile(path)
      if format == LIB_SUFFIX:
        self.writeAgdaLibFile(path)
      raise ValueError(" " + format + " no supported")

    def readInfoFromLibFile(self):
      return readLibFile(self.getLibFilePath())    

@pw.register_model('word')
class Keyword(db.Entity):
    word = PrimaryKey(str)
    libVersions = Set(LibraryVersion)
    libraries = Set(Library)

    def __str__(self):
      return self.word

    def __repr__(self):
      return self.word


@pw.register_model('agdaVersion')
class TestedWith(db.Entity):
    agdaVersion = PrimaryKey(str, auto=True)
    libraries = Set(LibraryVersion)
    
    def __str__(self):
      return "agda-" + self.agdaVersion

    def __repr__(self):
      return "agda-" + self.agdaVersion
        


class Dependency(db.Entity):
    id = PrimaryKey(int, auto=True)
    library = Required(Library)
    minVersion = Optional(str, default="")
    maxVersion = Optional(str, default="")
    supporting = Set(LibraryVersion)

    def __str__(self):
      text = self.minVersion \
        + ("<=" if self.minVersion else "") \
        + self.library.name \
        + ("<=" if self.maxVersion else "") \
        + self.maxVersion
      return text 

    def __repr__(self):
      return str(self)

try:
  db.bind('sqlite', DATABASE_FILE_PATH.as_posix(), create_db=True)
  db.generate_mapping(create_tables=True)
except Exception as e:
  logger.error(e)
