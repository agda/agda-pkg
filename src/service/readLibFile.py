'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import sys
import yaml

from pathlib  import Path
from pprint   import pprint

# ----------------------------------------------------------------------------

def readLibLegacyFile(fname):
  info = { "name": "", "version": "",  "include": [], "depend":[]}
  libraryfile = Path(fname)

  assert libraryfile.exists()
  assert libraryfile.suffix == ".agda-lib"

  with libraryfile.open('r') as f:
    content = sum([ line.strip().split() for line in f.readlines()],[])

    # name field
    try:
      indexName = content.index("name:")
      name = content[indexName + 1]
      info["name"] = name.strip()
    except Exception as e:
      # print("[!] 'name' field not found ==> using filename instead.")
      info["name"] = libraryfile.name.split(libraryfile.suffix)[0]

    # version field
    try:
      versionName = content.index("version:")
      version = content[versionName + 1]
      info["version"] = version.strip()
    except Exception as e:
      info["version"] = ""

    # include field
    indexInclude = content.index("include:")
    i = indexInclude + 1
    while i < len(content) and \
      (not "--" in content[i]) and \
      (not ":"  in content[i]) :
      pathinclude = content[i].strip()
      info["include"].append(content[i].strip())
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
      except Exception as e:
        pass
    except Exception as e:
      pass
  return info

def readPkgFile(fname):
  libraryfile = Path(fname)
  assert libraryfile.exists()
  assert libraryfile.suffix == ".agda-pkg"

  stream = libraryfile.open("r")
  docs = yaml.load_all(stream)
  info = [ doc for doc in docs ][0]
  assert "name" in info.keys() and "include" in info.keys()
  return info

def readLibFile(fname):
  libraryfile = Path(fname)
  if libraryfile.suffix == ".agda-lib":
    return readLibLegacyFile(fname)
  if libraryfile.suffix == ".agda-pkg":
    return readPkgFile(fname)
  return None
