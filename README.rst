Simple setup for Python scripts
###############################

:date: 2020-12-08
:tags: python, setup, scripts
:author: Roland Smith

.. Last modified: 2022-01-29T22:28:03+0100

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

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

To apply it to your project:

1) Copy ``simple.py`` or ``self-contained.py`` to ``setup.py`` in your
   project.
2) On UNIX-like systems, make sure ``setup.py`` is executable.
3) Edit the ``SCRIPTS`` tuple to contain the configuration data mentioned below.
4) Ensure that the installed name(s) for self-contained scripts are ignored by
   your revision control software.

To *use* it in your project:

Go to your project directory in a shell or ``cmd.exe`` window.
Run ``./setup.py`` to see the options and where the scripts would be
installed.
Run ``./setup.py install`` to install the scripts.
Run ``./setup.py uninstall`` to uninstall the scripts when they are installed.
For self-contained scripts, run ``./setup.py clean`` to remove generated
files.


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
  This is associated with ``python.exe``.
* ``.pyw`` for a Python script that uses a GUI toolkit. This is associated
  with ``pythonw.exe``, so that it doesn't show a superfluous ``cmd.exe``
  window on startup.

On ``posix``, installed scripts do not have an extension, and GUI scripts or
self-contained archives are handled automatically.

So, to prevent a whole lot of detection logic (there are e.g. many possible
GUI toolkits), the developer has to specify a 2-tuple or 4-tuple for each
script that has to be installed. This is called ``scripts``.

For ``simple.py`` this tuple contains:

* The name of the script in the source directory,
* the extension that has to be used for the installed script on the ``nt``
  platform.

For ``self-contained.py`` this tuple contains:

* The base name of the installed program.
* The name of the module (directory) it should contain.
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
