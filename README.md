agda-pkg [![PyPI version](https://badge.fury.io/py/agda-pkg.svg)](https://badge.fury.io/py/agda-pkg) [![Build Status](https://travis-ci.org/apkgbot/agda-pkg.svg?branch=master)](https://travis-ci.org/apkgbot/agda-pkg)
========


The Agda package manager that we all have been waiting for ~~so long~~.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Quick Start](#quick-start)
- [Usage](#usage)
	- [Initialisation of the package index](#initialisation-of-the-package-index)
	- [Help command](#help-command)
	- [Upgrade package indexed](#upgrade-package-indexed)
	- [List all the packages available](#list-all-the-packages-available)
	- [Installation of packages](#installation-of-packages)
	- [Uninstalling a package](#uninstalling-a-package)
	- [See packages installed](#see-packages-installed)
	- [Approximate search of packages](#approximate-search-of-packages)
	- [Get all the information of a package](#get-all-the-information-of-a-package)

<!-- /TOC -->

# Quick Start

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/installation.gif"
 alt="agda package manager installation" width=256 align="right" />


To install `agda-pkg`, you must have installed `Python 3.6+` or a latter version
on your machine. In addition, the python package manager `pip 18.0+`.

We have tested `agda-pkg` with `Agda v2.5.4+`.

Installing using Pypi

```
    $ pip install agda-pkg
```

Now, we can run the package manager using the command `agda-pkg` or even
shorter just `apkg`.

# Usage

## Initialisation of the package index

The easiest way to get libraries is from [the package index].
We will use this index to download and to install
Agda libraries. In addition, `agda-pkg` use a database to
maintain a register of all libraries available. To initialise
the index and the database run the following command:

```
    $ apkg init
    Indexing libraries from https://github.com/apkgbot/package-index.git
```

## Help command

```
    $ apkg --help
```

## Upgrade package indexed

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
same list.

## Installation of packages

We have three possibilities to install a package:


<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/index-stdlib.gif"
 alt="agda package manager installation" width=350 align="right" />

 -   from the [package index](http://github.com/apkgbot/package-index)

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

To see all the options, check out the help:

```
    $ apkg install --help
```

In addition, you may want to install multiple libraries at once

```
    $ apkg install standard-library agda-prop agda-metis
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

  [the package index]: https://github.com/apkgbot/package-index
  [local directory]: https://agda.readthedocs.io/en/v2.5.4/tools/package-system.html
  [PR]: https://github.com/apkgbot/package-index/pull/new/master
