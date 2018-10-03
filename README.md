agda-pkg [![PyPI version](https://badge.fury.io/py/agda-pkg.svg)](https://badge.fury.io/py/agda-pkg) [![Build Status](https://travis-ci.org/apkgbot/agda-pkg.svg?branch=master)](https://travis-ci.org/apkgbot/agda-pkg)
========

The Agda package manager that we all have been waiting for. This
tool do not modify `Agda` at all, it will just manage systematically the directory
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
		- [Installation of multiple packages at once](#installation-of-multiple-packages-at-once)
	- [Uninstalling a package](#uninstalling-a-package)
	- [See packages installed](#see-packages-installed)
	- [Approximate search of packages](#approximate-search-of-packages)
	- [Get all the information of a package](#get-all-the-information-of-a-package)
- [Creating a library for Agda-Pkg](#creating-a-library-for-agda-pkg)
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

The easiest way to get some libraries s by using [the package index]. We will use this index to download and to install
the libraries. In addition, `agda-pkg` use a local database to
maintain a register of all libraries available in your system. To initialise the index and the database run the following command:

```
    $ apkg init
    Indexing libraries from https://github.com/apkgbot/package-index.git
```

## Help command

Check all the options of a command or subcommand by using the flag `--help`.

```
    $ apkg --help
```

## Upgrade the package index

Recall updating the index every once in a while

```
    $ apkg upgrade
    Updating Agda-Pkg from https://github.com/apkgbot/package-index.git
```

If you want to index your library make a [PR] in [the package index]

## List all the packages available

To see all the package available run the following command:

```
    $ apkg list
```

This command also has the flag `--short` to display a short version of the
same list. For instance,

```
    $ apkg list --short
    Name                 Last version         Description
    -----------------------------------------------------
    agda-metis           v0.2.1               Missing.
    agda-prelude         4e0caf0              Missing.
    agda-prop            v0.1.2               Missing.
    agdarsec             v0.1.1               Missing.
    alga-theory          0fdb96c              Missing.
    fotc                 apia-1.0.2           Missing.
    hott-core            937e227              Missing.
    hott-theorems        937e227              Missing.
    standard-library     v0.16.1              Missing.
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

-   from a github repository

```
    $ apkg install --github agda/agda-stdlib --version v0.16
```

-   from a git repository

```
    $ apkg install http://github.com/jonaprieto/agda-prop.git
```

- from a tar ball file (coming soon).

### Installation of multiple packages at once

We may want to install multiple libraries at once,
so we have two options:

1. Using the inline method

```
    $ apkg install standard-library agda-prop agda-metis
```

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


Lastly, to see all the options, pleasee check out the help information:

```
    $ apkg install --help
```

## Uninstalling a package

Uninstall a package by default, just hide the library for Agda but no
remove the sources:

```
    $ apkg uninstall standard-library
```

If you want to remove completely the source and everything, use
remove-cache flag.

```
    $ apkg uninstall standard-library --remove-cache
```

## See packages installed


```
    $ apkg freeze
```

Useful to save the versions used for each library:


```
    $ apkg freeze > requirements.txt
```

You may want to install from the requirements file:


```
    $ apkg install < requirements.txt
```

## Approximate search of packages

We make a search (approximate) by using keywords and title of the
packages in the index. To perform such a search, see the following
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
    library: agda-prop
    sha: 6b2ea8e099ac6968004ec57d96f19b46bcb081ff
```

# Creating a library for Agda-Pkg

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
version:           0.0.1
author:            AuthorName
category:          [ classic, logic, theorems ]
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
