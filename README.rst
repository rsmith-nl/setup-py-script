Simple setup for Python scripts
###############################

:date: 2020-12-08
:tags: python, setup, scripts
:author: Roland Smith

.. Last modified: 2022-01-17T10:11:34+0100

Introduction
============

Installing Python scripts (as opposed to modules) is a too involved using
distutils/setuptools. Those do not take into account zipped archives and scripts using
a GUI toolkit.

So these setup scripts are an attempt to do things differently.
The goal is to provide (simple) installation for standalone scripts that may
or may not be compressed and that may or may not use a GUI.

Scripts that use their own module are wrapped up in a self-contained zip-file,
so they can be installed as a single script.


Usage
=====

1) Copy ``simple.py`` or ``self-contained.py`` to ``setup.py`` in your
   project.
2) Edit the ``scripts`` list to contain the abovementioned configuration data.


Project structure for self-contained scripts
--------------------------------------------

A typical project directory for self-contained script(s) looks like this::

    project/
    ├── console.py
    ├── gui.py
    └── module
        ├── __init__.py
        ├── bar.py
        ├── core.py
        ├── foo.py
        └── version.py

In this case, this is an application that has both a console and a GUI
interface, both of which use the functionality in the module.


Configuration data
------------------

On the ``nt`` platform, installed Python scripts can have two different
extensions;
* ``.py`` for a normal Python command-line script.
* ``.pyw`` for a Python script that uses a GUI toolkit

On ``posix``, installed scripts do not have an extension, and GUI scripts or
self-contained archives are handled automatically.

So, to prevent a whole lot of detection logic (there are e.g. many possible
GUI toolkits), the developer has to specify a 2-tuple or 4-tuple for each
script that has to be installed.

For ``simple.py`` this tuple contains:

* The name of the script in the source directory,
* the extension that has to be used for the installed script on the ``nt``
  platform.

For ``self-contained.py`` this tuple contains:

* The base name of the installed program.
* The name of the module it should contain.
* The name of the main file for the program. This should run the application
* the extension that has to be used for the installed script on the ``nt``
  platform.


Background
==========

Sysconfig data
--------------

The ``sysconfig`` module yields information about paths on the system Python
is installed on.
On FreeBSD UNIX (an example of a “posix” system):

.. code-block:: python

    In [1]: import sysconfig

    In [2]: import os

    In [3]: os.name
    Out[3]: 'posix'

    In [4]: sysconfig.get_scheme_names()
    Out[4]:
    ('nt',
    'nt_user',
    'osx_framework_user',
    'posix_home',
    'posix_prefix',
    'posix_user')

    In [5]: sysconfig.get_path("scripts", 'posix_home')
    Out[5]: '/usr/local/bin'

    In [6]: sysconfig.get_path("scripts", 'posix_user')
    Out[6]: '/home/rsmith/.local/bin'

On ms-windows:

.. code-block:: python

    >>> import os
    >>> os.name
    'nt'
    >>> import sysconfig
    >>> sysconfig.get_path("scripts", os.name + "_user")
    'C:\\Users\\Roland Smith\\AppData\\Roaming\\Python\\Python37\\Scripts'
    >>> sysconfig.get_path("scripts", os.name)
    'C:\\_LocalData\\Python3\\Scripts'


Installation scheme
-------------------

Since I prefer to have scripts installed without requiring root/administrator
access, I will use the following scheme.

* On ``posix`` systems, install using the ``posix_user`` scheme.
* On ``nt`` systems, first try the ``nt`` scheme, then ``nt_user``.