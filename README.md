agda-pkg [![PyPI version](https://badge.fury.io/py/agda-pkg.svg)](https://badge.fury.io/py/agda-pkg) [![Build Status](https://travis-ci.org/apkgbot/agda-pkg.svg?branch=master)](https://travis-ci.org/apkgbot/agda-pkg)
========

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/installation.gif"
 alt="agda package manager installation" width=256 align="right" />
 
The Agda package manager that we all are waiting for so long.

**Quick Start**

We need to have installed `Python 3.6+` or a latter version and `pip` to install
Python packages.

1.  Installation from Pypi

```
    $ pip install agda-pkg
```

2.  Initialisation of the package index

```
    $ apkg init
    Indexing libraries from https://github.com/apkgbot/package-index.git
```

3.  Check other options with the help flag

```
    $ apkg --help
```

4.  Recall updating the index every once in a while

```
    $ apkg upgrade
    Updating Agda-Pkg from https://github.com/apkgbot/package-index.git
```

If you want to index your library make a PR in [the package index]

**Installation of packages**

We have three possibilities to install a package:

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/index-stdlib.gif"
 alt="agda package manager installation" width=256 align="right" />

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

-   from the [package index](http://github.com/apkgbot/package-index)

<img src="https://github.com/apkgbot/agda-pkg/raw/master/assets/finished-stdlib.gif"
 alt="apkg install standard-library" width=256 align="right" />

```
    $ apkg install standard-library
```

To see all the options, check out the help:

```
    $ apkg install --help
```

In addition, you may want to install multiple libraries at once

```
    $ apkg install standard-library agda-prop agda-metis
```

**Uninstalling**

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

**See packages installed**

```
    $ apkg freeze
    agda-metis==a8df5b74ea2e0c007f0b7ffe24d440a35e1c6d94
    agda-prop==0.1.1
```

Useful to save the exact versions of your environment:


```
    $ apkg freeze > requirements.txt
```


**Search packages**

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

**Get information of a package**


```
    $ apkg info agda-prop
    library: agda-prop
    sha: 6b2ea8e099ac6968004ec57d96f19b46bcb081ff
```

  [the package index]: https://github.com/apkgbot/package-index.git
  [local directory]: https://agda.readthedocs.io/en/v2.5.4/tools/package-system.html
