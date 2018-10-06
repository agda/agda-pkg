agda-pkg [![PyPI version](https://badge.fury.io/py/agda-pkg.svg)](https://badge.fury.io/py/agda-pkg) [![Build Status](https://travis-ci.org/apkgbot/agda-pkg.svg?branch=master)](https://travis-ci.org/apkgbot/agda-pkg)
========

The Agda package manager that we all have been waiting for. This
tool does not modify `Agda` at all, it will just manage systematically the directory
`.agda` and its files: `.agda/defaults` and `.agda/libraries`.
For more information about how the Agda package system works, read
the official documentation [here](https://agda.readthedocs.io/en/v2.5.4.1/tools/package-system.html).

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/demo.gif"
 alt="agda package manager installation" height=500 align="right" />

**Table of contents**

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Quick Start](#quick-start)
- [Usage](#usage)
	- [Initialisation of the package index](#initialisation-of-the-package-index)
	- [Help command](#help-command)
	- [Upgrade the package index](#upgrade-the-package-index)
	- [List all the packages available](#list-all-the-packages-available)
	- [Installation of packages](#installation-of-packages)
		- [Multiple packages at once](#multiple-packages-at-once)
	- [Uninstalling a package](#uninstalling-a-package)
	- [Update a package to latest version](#update-a-package-to-latest-version)
	- [See packages installed](#see-packages-installed)
	- [Approximate search of packages](#approximate-search-of-packages)
	- [Get all the information of a package](#get-all-the-information-of-a-package)
- [Creating a library with Agda-Pkg](#creating-a-library-for-agda-pkg)
	- [Directory structure of an agda library](#directory-structure-of-an-agda-library)
	- [.agda-lib library file](#agda-lib-library-file)
	- [.agda-pkg library file](#agda-pkg-library-file)
- [About](#about)

<!-- /TOC -->

# Quick Start

To install `agda-pkg`, you must have installed `Python 3.6+` or a latter version
on your machine. In addition, the python package manager `pip 18.0+`.

We have tested `agda-pkg` with `Agda v2.5.4+`.

Installing using `pip`:

```
    $ pip install agda-pkg
```

Now, we can run the package manager using the command `agda-pkg` or even
shorter just `apkg`.

# Usage

## Initialisation of the package index

The easiest way to get some libraries is by using [the package index].
We will use this index to download and to install the libraries. In
addition, `agda-pkg` uses a local database to maintain a register of
all libraries available in your system. To initialise the index and
the database please run the following command:

```
    $ apkg init
    Indexing libraries from https://github.com/apkgbot/package-index.git
```

**Note**.
To use a different location for the files `defaults` and `libraries` for Agda,
you can set up the environment variable `AGDA_DIR` as fallows.

```
    $ export AGDA_DIR=$HOME/.agda
```

Other way is to create a directory `.agda` in your directory and run
`agda-pkg` from that directory. `agda-pkg` will prioritize the `.agda`
directory in the current directory.

## Help command

Check all the options of a command or subcommand by using the flag `--help`.

```
    $ apkg --help
    $ apkg install --help
```

## Upgrade the package index

Recall updating the index every once in a while using `upgrade`.

```
    $ apkg upgrade
    Updating Agda-Pkg from https://github.com/apkgbot/package-index.git
```

If you want to index your library go to [the package index] and make [PR].

## List all the packages available

To see all the package available run the following command:

```
    $ apkg list
```

This command also has the flag `--short` to display a short version of the
same list.

```
    $ apkg list --short
    Name                 Last version         Description
    -----------------------------------------------------
    agda-metis           v0.2.1               
    agda-prelude         4e0caf0              
    agda-prop            v0.1.2               
    agdarsec             v0.1.1               
    alga-theory          0fdb96c              
    fotc                 apia-1.0.2           
    hott-core            937e227              
    hott-theorems        937e227              
    standard-library     v0.16.1              
```

## Installation of packages

Install a library is now easy. We have multiple ways to install a package.

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/index-stdlib.gif"
 alt="agda package manager installation" width=350 align="right" />

 -   from the [package-index](http://github.com/apkgbot/package-index)

 ```
     $ apkg install standard-library
 ```

-   from a [local directory]

```
    $ apkg install .
```

or simpler:

```
    $ apkg install
```

-   from a github repository

```
    $ apkg install --github agda/agda-stdlib --version v0.16
```

-   from a git repository

```
    $ apkg install http://github.com/jonaprieto/agda-prop.git
```

To specify the version of a library, we use the flag `--version`

```
    $ apkg install standard-library --version v0.16.1
```

Or simpler by using `@` or `==` as it follows.

```
    $ apkg install standard-library@v0.16.1
    $ apkg install standard-library==v0.16.1
```

### Multiple packages at once

To install multiple libraries at once, we have two options:

1. Using the inline method

```
    $ apkg install standard-library agda-prop agda-metis
```

Use `@` or `==` if you need a specific version, see above
examples.

2. Using a requirement file:

Generate a requirement file using `apkg freeze`:

```
    $ apkg freeze > requirements.txt
    $ cat requirements.txt
    agda-metis==0.1
    agda-prop==0.1.1
````

Now, use the flag `-r` to install all the listed libraries
in this file:

```
    $ apkg install -r requirements.txt
```


Check all the options of this command with the help information:

```
    $ apkg install --help
```

## Uninstalling a package

Uninstalling a package will remove the library from the visible libraries for Agda.

```
    $ apkg uninstall standard-library
```

But if you want to remove the library completely (the sources and everything) you
should use the flag `--remove-cache`.

```
    $ apkg uninstall standard-library --remove-cache
```

## Update a package to latest version

We can get the latest version of a package from
the versions registered in the package-index.

- Update all the installed libraries:

```
    $ apkg update
```

- Update a specific list of libraries. If some
library is not installed, this command will installed
the latest version of it.

```
    $ apkg update standard-library agdarsec
```

## See packages installed


```
    $ apkg freeze
    agda-metis==v0.2.1
    agda-prop==v0.1.2
    standard-library==v0.16
```

This command is useful to keep in a file the versions used for your project
to install them later.


```
    $ apkg freeze > requirements.txt
```

To install from this requirement file run this command.


```
    $ apkg install < requirements.txt
```

## Approximate search of packages

We make a search (approximate) by using keywords and title of the
packages from the index. To perform such a search, see the following
example:


```
    $ apkg search metis
    1 result in 0.0026731969992397353seg
    matches: {'name': [b'agda-metis']}

    agda-metis
    ==========
    url: https://github.com/jonaprieto/test-agdapkgbot.git
```

## Get all the information of a package


```
    $ apkg info agda-prop
    library: standard-library
    sha: a1a10b39d35b8fc40e87723a89f5682252d46380
    include: src/
    depend: []
    installed: True
    cached: True
    fromIndex: False
    fromUrl: False
    fromGit: True
    origin: https://github.com/agda/agda-stdlib.git
    version: v0.16
    default: True
    --------------------------------------------------
    versions: v0.16.1,v0.16
```

# Creating a library for Agda-Pkg

In this section, we describe how to build a library.

To build a project using `agda-pkg`, we just run the following command:

```
    $ apkg create
```

Some questions are going to be prompted in order to create
the necessary files for Agda and for Agda-Pkg.

The output is a folder like the following showed below.

## Directory structure of an agda library

A common Agda library has the following structure:

```
$ tree -L 1 mylibrary/
mylibrary/
├── LICENSE
├── README.md
├── mylibrary.agda-lib
├── mylibrary.agda-pkg
├── src
└── test

2 directories, 3 files
```

## .agda-lib library file

```yaml
$ cat mylibrary.agda-lib
name: mylibrary  -- Comment
depend: LIB1 LIB2
  LIB3
  LIB4
include: PATH1
  PATH2
  PATH3
```

## .agda-pkg library file

This file only works for `agda-pkg`. The idea of
this file is to provide more information about the
package, pretty similar to the cabal files in Haskell.
This file has priority over its version `.agda-lib`.

```yaml
$ cat mylibrary.agda-pkg
name:              mylibrary
version:           v0.0.1
author:            
    - AuthorName1
    - AuthorName2
category:          cat1, cat2, cat3
homepage:          http://github.com/user/mylibrary
license:           MIT
license-file:      LICENSE.md
source-repository: http://github.com/user/mylibrary.git
tested-with:       2.5.6
description:       Put here a description.

include:
    - PATH1
    - PATH2
    - PATH3
depend:
    - LIB1
    - LIB2
    - LIB3
    - LIB4
```

  [the package index]: https://github.com/apkgbot/package-index
  [local directory]: https://agda.readthedocs.io/en/v2.5.4/tools/package-system.html
  [PR]: https://github.com/apkgbot/package-index/pull/new/master

# About

This is a proof of concept of an Agda Package Manager.
The Haskell version is in a [very early stage](http://github.com/jonaprieto/agda-pkg).

Any contribution or feedback to improve this work is very welcomed.
