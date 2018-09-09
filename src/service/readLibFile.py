'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import sys
import yaml

from pathlib import Path
from pprint import pprint

def readLibLegacyFile(fname):
  info = { "name": "",  "include": [], "depend":[]}
  libraryfile = Path(fname)
  assert libraryfile.suffix == ".agda-lib"

  with libraryfile.open('r') as f:
    content = sum([ line.strip().split() for line in f.readlines()],[])

    # name field
    indexName = content.index("name:")
    name = content[indexName + 1]
    info["name"] = name.strip()

    # include field
    indexInclude = content.index("include:")
    i = indexInclude + 1
    while i < len(content) and \
      (not "--" in content[i]) and \
      (not ":"  in content[i]) :
      pathinclude = content[i].strip()
      info["include"].append(content[i].strip())
      if not Path(pathinclude).exists() :
        print("Warning: the path (" + pathinclude + ") doesn't exist")
      i += 1
    info["include"] = list(set(info["include"]))

    # depend field
    try:
      indexDepend = content.index("depend:")
      i = indexDepend + 1
      try:
        while i < len(content) and \
          (not "--" in content[i]) and \
          (not ":"  in content[i]) :
          info["depend"].append(content[i].strip())
          i += 1
        info["depend"] = list(set(info["depend"]))
      except Exception(e):
        print("Error: malformed depend field")
    except ValueError:
      print("Error: malformed depend field")
    pprint(info)

def readLibYAMLFile(fname):
  libraryfile = Path(fname)
  assert libraryfile.suffix == ".agda-pkg"

  stream = libraryfile.open("r")
  docs = yaml.load_all(stream)
  info = [ doc for doc in docs ][0]
  assert "name" in info.keys() and "include" in info.keys()

  for pathinclude in info["include"]:
    if not Path(pathinclude).exists() :
      print("Warning: the path (" + pathinclude + ") doesn't exist")

  pprint(info)
  return docs

def readLibFile(fname):
  libraryfile = Path(fname)
  if libraryfile.suffix == ".agda-lib":
    return readLibLegacyFile(fname)
  if libraryfile.suffix == ".agda-pkg":
    return readLibYAMLFile(fname)
  print( libraryfile.suffix.as_posix() + " is not supported")
