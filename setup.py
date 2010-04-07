import shutil
import os
import subprocess
import re

from os.path \
    import \
        join, basename, dirname
from glob \
    import \
        glob

import setuptools
from setuptools.command.install \
    import \
        install as old_install
from distutils.core \
    import \
        setup

VERSION = "0.0.2"
RELEASED = False

try:
    if os.path.exists(".git"):
        s = subprocess.Popen(["git", "rev-parse", "HEAD"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = s.communicate()[0]
        GIT_REVISION = out.strip()
    else:
        GIT_REVISION = ""
except WindowsError:
    GIT_REVISION = ""

if not RELEASED:
    FULL_VERSION = VERSION + "dev"
else:
    FULL_VERSION = VERSION

def generate_version_py(filename):
    cnt = """\
# This file was autogenerated
version = '%s'
git_revision = '%s'
"""
    cnt = cnt % (FULL_VERSION, GIT_REVISION)

    f = open(filename, "w")
    try:
        f.write(cnt)
    finally:
        f.close()

def create_ply_tabfile():
    from toydist.core.parser.parser import parse
    parse('')

class install(old_install):
    def initialize_options(self):
        old_install.initialize_options(self)
        self.__files = []

    def _copy(self, source, target):
        if not os.path.exists(dirname(target)):
            os.makedirs(dirname(target))
        shutil.copy(source, target)
        self.__files.append(target)

    def run(self):
        create_ply_tabfile()

        self._copy(join("toydist", "parsetab"),
                   join(self.install_purelib, "toydist", "parsetab"))

        tdir = join(self.install_platlib, "toydist", "commands", "wininst")
        for source in glob(join("toydist", "commands", "wininst", "*.exe")):
            target = join(tdir, basename(source))
            self._copy(source, target)

        source = join("toydist", "commands", "cli.exe")
        target = join(self.install_platlib, "toydist", "commands", "cli.exe")
        self._copy(source, target)

        # MUST be run after __files contains everything
        old_install.run(self)

    def get_outputs(self):
        outfiles = old_install.get_outputs(self)
        outfiles.extend(self.__files)
        return outfiles

DESCR = """\
Toydist is a toy distribution tool for python packages, The goal are
extensibility, flexibility, and easy interoperation with external tools.

Toydist is still in infancy; discussions happen on the NumPy Mailing list
(http://mail.scipy.org/pipermail/numpy-discussion/).
"""

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS"
]

METADATA = {
    'name': 'toydist',
    'version': FULL_VERSION,
    'description': 'A toy distribution tool',
    'url': 'http://github.com/cournape/toydist',
    'author': 'David Cournapeau',
    'author_email': 'cournape@gmail.com',
    'license': 'BSD',
    'long_description': DESCR,
    'platforms': 'any',
    'classifiers': CLASSIFIERS,
}

PACKAGE_DATA = {
    'packages': ['toydist', 'toydist.core', 'toydist.commands', 'toydist.private',
                 'toymakerlib', 'toydist.core.platforms', 'toydist.core.parser'],
    'entry_points': {
        'console_scripts': ['toymaker=toymakerlib.toymaker:noexc_main']
    },
    'cmdclass': {"install": install}
}

if __name__ == '__main__':
    generate_version_py("toydist/__dev_version.py")
    config = {}
    for d in (METADATA, PACKAGE_DATA):
        for k, v in d.items():
            config[k] = v
    setup(**config)
