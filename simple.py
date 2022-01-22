#!/usr/bin/env python
# file: setup.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2020-10-25T12:18:04+0100
# Last modified: 2022-01-22T09:38:59+0100
"""Script to install scripts for the local user."""

import os
import shutil
import sys
import sysconfig

# What to install
scripts = [("cmdline.py", ".py"), ("tk-gui.py", ".pyw")]

# Preparation
if os.name == "posix":
    destdir = sysconfig.get_path("scripts", "posix_user")
    destdir2 = ""
elif os.name == "nt":
    destdir = sysconfig.get_path("scripts", os.name)
    destdir2 = sysconfig.get_path("scripts", os.name + "_user")
else:
    print(f"The system '{os.name}' is not recognized. Exiting")
    sys.exit(1)
cmd = None
if len(sys.argv) == 2:
    cmd = sys.argv[1].lower()
if cmd == "install":
    if not os.path.exists(destdir):
        os.makedirs(destdir)
elif cmd == "uninstall":
    pass
else:
    print(f"Usage {sys.argv[0]} [install|uninstall]")
# Actual (de)installation.
for script, nt_ext in scripts:  # noqa
    base = os.path.splitext(script)[0]
    if os.name == "posix":
        destname = destdir + os.sep + base
        destname2 = ""
    elif os.name == "nt":
        destname = destdir + os.sep + base + nt_ext
        destname2 = destdir2 + os.sep + base + nt_ext
    if cmd == "install":
        for d in (destname, destname2):
            try:
                shutil.copyfile(script, d)
                print(f"* installed '{script}' as '{d}'.")
                os.chmod(d, 0o700)
                break
            except (OSError, PermissionError, FileNotFoundError):
                pass  # Can't write to destination
        else:
            print(f"! installation of '{script}' has failed.")
    elif cmd == "uninstall":
        for d in (destname, destname2):
            try:
                os.remove(d)
                print(f"* removed '{d}'")
            except FileNotFoundError:
                pass  # path doesn't exist
    else:
        print(f"* '{script}' would be installed as '{destname}'")
        if destname2:
            print(f"  or '{destname2}'")
