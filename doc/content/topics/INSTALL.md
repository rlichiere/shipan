# Quick install guide

Before you can use ShipanShop, you'll need to get it installed. We have a
[complete installation guide](/doc/content/topics/advanced/INSTALL_GUIDE.md) that covers all the
possibilities; this guide will guide you to a minimal installation that'll work
while you walk through the introduction.

## Install Python

Using a Python Web framework, Shipan requires Python and Django. See
[FAQ](FAQ.md) for details. Python includes a lightweight
database called [SQLite](https://sqlite.org/) so you won't need to set up a database just yet.

Shipan is actually compatible with Python 2.7 and Django 1.11.

You can verify that Python is installed by typing ``python`` from your shell ;
you should see something like:
```
    Python 2.7.y
    [GCC 4.x] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
```

## Set up a database

This step is only necessary if you'd like to work with a "large" database engine
like PostgreSQL, MariaDB, MySQL, or Oracle. To install such a database, consult
the _database installation information_ in Django documentation.

## Install Shipan

You've got three options to install Shipan:

* [Install an official release](/doc/content/topics/advanced/INSTALL_GUIDE.md#official). This
  is the best approach for most users.

* [Install the latest development version](/doc/content/topics/advanced/INSTALL_GUIDE.md#development).
  This option is for enthusiasts who want
  the latest-and-greatest features and aren't afraid of running brand new code.
  You might encounter new bugs in the development version, but reporting them
  helps the development of Shipan. Also, releases of third-party packages are
  less likely to be compatible with the development version than with the
  latest stable release.

## Verifying

To verify that Shipan can be seen by Python, type ``python`` from your shell.
Then at the Python prompt, try to import Shipan:

```
    >>> import shipan
    >>> print(shipan.get_version())
    |version|
```

## That's it!

That's it -- you can now [move onto the tutorial](/doc/content/topics/tutorial/TUTORIAL_01.md).