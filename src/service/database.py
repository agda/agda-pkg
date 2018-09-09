
from ..config import DATABASE_FILE_NAME, DATABASE_FILE_PATH
from ..config import DATABASE_SERACHINDEXES_PATH
from ..config import INDEX_REPOSITORY_PATH

from pony.orm    import *
from ponywhoosh  import PonyWhoosh

# --------------------------------------------------------------------

pw = PonyWhoosh()

# configurations
pw.indexes_path          = DATABASE_SERACHINDEXES_PATH
pw.search_string_min_len = 1
pw.writer_timeout        = 3

db = Database()

@pw.register_model('name', 'description', 'url')
class Library(db.Entity):
    name = PrimaryKey(str)
    description = Optional(str, nullable=True)
    url = Optional(str, nullable=True)
    versions = Set('LibraryVersion')
    installed = Optional(bool, default=False)
    appearson = Set('Dependency')
    localpath = Optional(str)

@pw.register_model('version', 'gitURL', 'sha', 'description', 'license')
class LibraryVersion(db.Entity):
    library = Required(Library)
    version = Optional(str)
    gitURL = Optional(str)
    sha = Optional(str)
    description = Optional(str)
    license = Optional(str)
    testedWith = Set('TestedWith')
    keywords = Set('Keyword')
    requires = Set('Dependency')

@pw.register_model('word')
class Keyword(db.Entity):
    word = PrimaryKey(str)
    library_version = Optional(LibraryVersion)

@pw.register_model('agdaVersion')
class TestedWith(db.Entity):
    agdaVersion = PrimaryKey(str, auto=True)
    libraries = Set(LibraryVersion)

class Dependency(db.Entity):
    id = PrimaryKey(int, auto=True)
    library = Required(Library)
    minVersion = Optional(str)
    maxVersion = Optional(str)
    supporting = Set(LibraryVersion)

db.bind('sqlite', DATABASE_FILE_PATH.as_posix(), create_db=True)
db.generate_mapping(create_tables=True)
