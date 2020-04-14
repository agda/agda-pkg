agda-pkg [![PyPI version](https://badge.fury.io/py/agda-pkg.svg)](https://badge.fury.io/py/agda-pkg) [![Build Status](https://travis-ci.org/agda/agda-pkg.svg?branch=master)](https://travis-ci.org/agda/agda-pkg)
========

This is a tool to manage Agda libraries with extra features like
installing libraries from different kind of sources. This tool does
not modify `Agda` at all, it just manages systematically the directory
`.agda` and the files: `.agda/defaults` and `.agda/libraries` used by
Agda to locate libraries. For more information about how Agda package
system works, please read the official documentation
[here](https://agda.readthedocs.io/en/v2.6.0/tools/package-system.html).

*Some common usages of Agda-Pkg*

-   `$ apkg install standard-library`
-   `$ apkg install --github agda/agda-stdlib --version v1.3`
-   `$ apkg install --github plfa/plfa.github.io --branch dev --name plfa`
-   `$ apkg install --editable .` (to use a library current in development)
-   `$ apkg uninstall standard-library`

After running `apkg init`, Agda-pkg can install some libraries from the index
[agda/package-index](http://github.com/agda/package-index), below you'll see
a list.


**Library name**         | **Latest version** | **URL**
-----|-----|-----
agda-base            | v0.2            		 | https://github.com/pcapriotti/agda-base.git
agda-categories      | v0.1            		 | https://github.com/agda/agda-categories.git
agda-metis           | v0.2.1          		 | https://github.com/jonaprieto/agda-metis.git
agda-prelude         | df679cf         		 | https://github.com/UlfNorell/agda-prelude.git
agda-prop            | v0.1.2          		 | https://github.com/jonaprieto/agda-prop.git
agda-real            | e1558b62        		 | https://gitlab.com/pbruin/agda-real.git
agda-ring-solver     | d1ed21c         		 | https://github.com/oisdk/agda-ring-solver.git
agdarsec             | v0.3.0          		 | https://github.com/gallais/agdarsec.git
alga-theory          | 0fdb96c         		 | https://github.com/algebraic-graphs/agda.git
ataca                | a9a7c06         		 | https://github.com/jespercockx/ataca.git
cat                  | v1.6.0          		 | https://github.com/fredefox/cat.git
cubical              | v0.1            		 | https://github.com/agda/cubical.git
FiniteSets           | c8c2600         		 | https://github.com/L-TChen/FiniteSets.git
fotc                 | apia-1.0.2      		 | https://github.com/asr/fotc.git
generic              | f448ab3         		 | https://github.com/effectfully/Generic.git
hott-core            | 1037d82         		 | https://github.com/HoTT/HoTT-Agda.git
hott-theorems        | 1037d82         		 | https://github.com/HoTT/HoTT-Agda.git
HoTT-UF-Agda         | 9d0f38e         		 | https://github.com/martinescardo/HoTT-UF-Agda-Lecture-Notes.git
ial                  | v1.5.0          		 | https://github.com/cedille/ial.git
lightweight-prelude  | b2d440a         		 | https://github.com/L-TChen/agda-lightweight-prelude.git
mini-hott            | d9b4a7b         		 | https://github.com/jonaprieto/mini-hott.git
MtacAR               | 5417230         		 | https://github.com/L-TChen/MtacAR.git
plfa                 | stable-web-2019.09        | https://github.com/plfa/plfa.github.io.git
routing-library      | thesis          		 | https://github.com/MatthewDaggitt/agda-routing.git
standard-library     | v1.3            		 | https://github.com/agda/agda-stdlib.git


<img src="https://github.com/agda/agda-pkg/raw/master/assets/demo.gif"
 alt="agda package manager installation" height=500 align="right" />

**Table of contents**

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Quick Start](#quick-start)
- [Usage](#usage)
	- [Initialisation of the package index](#initialisation-of-the-package-index)
	- [Help command](#help-command)
	- [Upgrade the package index](#upgrade-the-package-index)
    - [Environmental variables](#environmental-variables)
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
on your machine. In addition, the python package manager `pip3 18.0+` (for python 3).

We have tested `agda-pkg` with `Agda v2.5.4+`.

To install this tool run the following command:

```
    $ pip install agda-pkg
```

Now, we can run the package manager using the command `agda-pkg` or even
shorter just `apkg`.

# Usage

## Initialisation of the package index

The easiest way to install libraries is by using [the package index].
`agda-pkg` uses a local database to maintain a register of all
libraries available in your system. To initialize the index and the
database please run the following command:

```
    $ apkg init
    Indexing libraries from https://github.com/agda/package-index.git
```

**Note**. To use a different location for your agda files `defaults`
and `libraries`, you can set up the environment variable `AGDA_DIR`
before run `apkg` as follows:

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
    Updating Agda-Pkg from https://github.com/agda/package-index.git
```

If you want to index your library go to [the package index] and make [PR].

## Environmental variables

If there is an issue with your installation or you suspect something
is going wrong. You might want to see the environmental variables used by apkg.

```
    $ apkg environment
```


## List all the packages available

To see all the packages available run the following command:

```
    $ apkg list
```

This command also has the flag `--full` to display a version of the
this list with more details.


## Installation of packages

Install a library is now easy. We have multiple ways to install a package.

<img src="https://github.com/agda/agda-pkg/raw/master/assets/index-stdlib.gif"
 alt="agda package manager installation" width=350 align="right" />

 -   from the [package-index](http://github.com/agda/package-index)

 ```
     $ apkg install standard-library
 ```

-   from a [local directory]

```
    $ apkg install .
```

or even much simpler:

```
    $ apkg install
```

Installing a library creates a copy for agda in the directory assigned
by agda-pkg. If you want your current directory to be taken into
account for any changes use the `--editable` option.  as shown below.


```
    $ apkg install --editable .
```

-   from a github repository

```
    $ apkg install --github agda/agda-stdlib --version v1.1
```

-   from a git repository

```
    $ apkg install http://github.com/jonaprieto/agda-prop.git
```

To specify the version of a library, we use the flag `--version`

```
    $ apkg install standard-library --version v1.0
```

Or simpler by using `@` or `==` as it follows.

```
    $ apkg install standard-library@v1.0
    $ apkg install standard-library==v1.0
```

### Multiple packages at once

To install multiple libraries at once, we have two options:

1. Using the inline method

```
    $ apkg install standard-library agda-base
```

Use `@` or `==` if you need a specific version, see above
examples.

2. Using a requirement file:

Generate a requirement file using `apkg freeze`:

```
    $ apkg freeze > requirements.txt
    $ cat requirements.txt
    standard-library==v1.1
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

- using the name of the library

```
    $ apkg uninstall standard-library
```

- infering the library name from the current directory

```
    $ apkg uninstall .
```

And if we want to remove the library completely (the sources and
everything), we use the flag `--remove-cache`.

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
    standard-library==v1.1
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
    1 result in 0.0012656739999998834seg
    cubical
    url: https://github.com/agda/cubical.git
    installed: False
```

## Get all the information of a package


```
    $ apkg info cubical
   
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
tested-with:       2.6.0
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

  [the package index]: https://github.com/agda/package-index
  [local directory]: https://agda.readthedocs.io/en/v2.5.4/tools/package-system.html
  [PR]: https://github.com/agda/package-index/pull/new/master

# About

This is a proof of concept of an Agda Package Manager.
Any contribution or feedback to improve this work is very welcomed.
