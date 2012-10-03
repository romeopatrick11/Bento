ref = {'author': 'The fellowship of the packaging',
 'author_email': 'distutils-sig@python.org',
 'data_files': {},
 'description': '===============================\nInstalling and Using Distribute\n===============================\n\n.. contents:: **Table of Contents**\n\n-----------\nDisclaimers\n-----------\n\nAbout the fork\n==============\n\n`Distribute` is a fork of the `Setuptools` project.\n\nDistribute is intended to replace Setuptools as the standard method\nfor working with Python module distributions.\n\nThe fork has two goals:\n\n- Providing a backward compatible version to replace Setuptools\n  and make all distributions that depend on Setuptools work as\n  before, but with less bugs and behaviorial issues.\n\n  This work is done in the 0.6.x series.\n\n  Starting with version 0.6.2, Distribute supports Python 3.\n  Installing and using distribute for Python 3 code works exactly\n  the same as for Python 2 code, but Distribute also helps you to support\n  Python 2 and Python 3 from the same source code by letting you run 2to3\n  on the code as a part of the build process, by setting the keyword parameter\n  ``use_2to3`` to True. See http://packages.python.org/distribute for more\n  information.\n\n- Refactoring the code, and releasing it in several distributions.\n  This work is being done in the 0.7.x series but not yet released.\n\nThe roadmap is still evolving, and the page that is up-to-date is\nlocated at : `http://packages.python.org/distribute/roadmap`.\n\nIf you install `Distribute` and want to switch back for any reason to\n`Setuptools`, get to the `Uninstallation instructions`_ section.\n\nMore documentation\n==================\n\nYou can get more information in the Sphinx-based documentation, located\nat http://packages.python.org/distribute. This documentation includes the old\nSetuptools documentation that is slowly replaced, and brand new content.\n\nAbout the installation process\n==============================\n\nThe `Distribute` installer modifies your installation by de-activating an\nexisting installation of `Setuptools` in a bootstrap process. This process\nhas been tested in various installation schemes and contexts but in case of a\nbug during this process your Python installation might be left in a broken\nstate. Since all modified files and directories are copied before the\ninstallation starts, you will be able to get back to a normal state by reading\nthe instructions in the `Uninstallation instructions`_ section.\n\nIn any case, it is recommended to save you `site-packages` directory before\nyou start the installation of `Distribute`.\n\n-------------------------\nInstallation Instructions\n-------------------------\n\nDistribute is only released as a source distribution.\n\nIt can be installed using pip, and can be done so with the source tarball,\nor by using the ``distribute_setup.py`` script provided online.\n\n``distribute_setup.py`` is the simplest and preferred way on all systems.\n\ndistribute_setup.py\n===================\n\nDownload\n`distribute_setup.py <http://python-distribute.org/distribute_setup.py>`_\nand execute it, using the Python interpreter of your choice.\n\nIf your shell has the ``curl`` program you can do::\n\n    $ curl -O http://python-distribute.org/distribute_setup.py\n    $ python distribute_setup.py\n\nNotice this file is also provided in the source release.\n\npip\n===\n\nRun easy_install or pip::\n\n    $ pip install distribute\n\nSource installation\n===================\n\nDownload the source tarball, uncompress it, then run the install command::\n\n    $ curl -O http://pypi.python.org/packages/source/d/distribute/distribute-0.6.27.tar.gz\n    $ tar -xzvf distribute-0.6.27.tar.gz\n    $ cd distribute-0.6.27\n    $ python setup.py install\n\n---------------------------\nUninstallation Instructions\n---------------------------\n\nLike other distutils-based distributions, Distribute doesn\'t provide an\nuninstaller yet. It\'s all done manually! We are all waiting for PEP 376\nsupport in Python.\n\nDistribute is installed in three steps:\n\n1. it gets out of the way an existing installation of Setuptools\n2. it installs a `fake` setuptools installation\n3. it installs distribute\n\nDistribute can be removed like this:\n\n- remove the ``distribute*.egg`` file located in your site-packages directory\n- remove the ``setuptools.pth`` file located in you site-packages directory\n- remove the easy_install script located in you ``sys.prefix/bin`` directory\n- remove the ``setuptools*.egg`` directory located in your site-packages directory,\n  if any.\n\nIf you want to get back to setuptools:\n\n- reinstall setuptools using its instruction.\n\nLastly:\n\n- remove the *.OLD.* directory located in your site-packages directory if any,\n  **once you have checked everything was working correctly again**.\n\n-------------------------\nQuick help for developers\n-------------------------\n\nTo create an egg which is compatible with Distribute, use the same\npractice as with Setuptools, e.g.::\n\n    from setuptools import setup\n\n    setup(...\n    )\n\nTo use `pkg_resources` to access data files in the egg, you should\nrequire the Setuptools distribution explicitly::\n\n    from setuptools import setup\n\n    setup(...\n        install_requires=[\'setuptools\']\n    )\n\nOnly if you need Distribute-specific functionality should you depend\non it explicitly. In this case, replace the Setuptools dependency::\n\n    from setuptools import setup\n\n    setup(...\n        install_requires=[\'distribute\']\n    )\n\n-----------\nInstall FAQ\n-----------\n\n- **Why is Distribute wrapping my Setuptools installation?**\n\n   Since Distribute is a fork, and since it provides the same package\n   and modules, it renames the existing Setuptools egg and inserts a\n   new one which merely wraps the Distribute code. This way, full\n   backwards compatibility is kept for packages which rely on the\n   Setuptools modules.\n\n   At the same time, packages can meet their dependency on Setuptools\n   without actually installing it (which would disable Distribute).\n\n- **How does Distribute interact with virtualenv?**\n\n  Everytime you create a virtualenv it will install setuptools by default.\n  You either need to re-install Distribute in it right after or pass the\n  ``--distribute`` option when creating it.\n\n  Once installed, your virtualenv will use Distribute transparently.\n\n  Although, if you have Setuptools installed in your system-wide Python,\n  and if the virtualenv you are in was generated without the `--no-site-packages`\n  option, the Distribute installation will stop.\n\n  You need in this case to build a virtualenv with the `--no-site-packages`\n  option or to install `Distribute` globally.\n\n- **How does Distribute interacts with zc.buildout?**\n\n  You can use Distribute in your zc.buildout, with the --distribute option,\n  starting at zc.buildout 1.4.2::\n\n  $ python bootstrap.py --distribute\n\n  For previous zc.buildout versions, *the only thing* you need to do\n  is use the bootstrap at `http://python-distribute.org/bootstrap.py`.  Run\n  that bootstrap and ``bin/buildout`` (and all other buildout-generated\n  scripts) will transparently use distribute instead of setuptools.  You do\n  not need a specific buildout release.\n\n  A shared eggs directory is no problem (since 0.6.6): the setuptools egg is\n  left in place unmodified.  So other buildouts that do not yet use the new\n  bootstrap continue to work just fine.  And there is no need to list\n  ``distribute`` somewhere in your eggs: using the bootstrap is enough.\n\n  The source code for the bootstrap script is located at\n  `http://bitbucket.org/tarek/buildout-distribute`.\n\n\n\n-----------------------------\nFeedback and getting involved\n-----------------------------\n\n- Mailing list: http://mail.python.org/mailman/listinfo/distutils-sig\n- Issue tracker: http://bitbucket.org/tarek/distribute/issues/\n- Code Repository: http://bitbucket.org/tarek/distribute\n\n=======\nCHANGES\n=======\n\n------\n0.6.27\n------\n\n* Support current snapshots of CPython 3.3.\n* Distribute now recognizes README.rst as a standard, default readme file.\n* Exclude \'encodings\' modules when removing modules from sys.modules.\n  Workaround for \\#285.\n* Issue \\#231: Don\'t fiddle with system python when used with buildout\n  (bootstrap.py)\n\n------\n0.6.26\n------\n\n* Issue \\#183: Symlinked files are now extracted from source distributions.\n* Issue \\#227: Easy_install fetch parameters are now passed during the\n  installation of a source distribution; now fulfillment of setup_requires\n  dependencies will honor the parameters passed to easy_install.\n\n------\n0.6.25\n------\n\n* Issue \\#258: Workaround a cache issue\n* Issue \\#260: distribute_setup.py now accepts the --user parameter for\n  Python 2.6 and later.\n* Issue \\#262: package_index.open_with_auth no longer throws LookupError\n  on Python 3.\n* Issue \\#269: AttributeError when an exception occurs reading Manifest.in\n  on late releases of Python.\n* Issue \\#272: Prevent TypeError when namespace package names are unicode\n  and single-install-externally-managed is used. Also fixes PIP issue\n  449.\n* Issue \\#273: Legacy script launchers now install with Python2/3 support.\n\n------\n0.6.24\n------\n\n* Issue \\#249: Added options to exclude 2to3 fixers\n\n------\n0.6.23\n------\n\n* Issue \\#244: Fixed a test\n* Issue \\#243: Fixed a test\n* Issue \\#239: Fixed a test\n* Issue \\#240: Fixed a test\n* Issue \\#241: Fixed a test\n* Issue \\#237: Fixed a test\n* Issue \\#238: easy_install now uses 64bit executable wrappers on 64bit Python\n* Issue \\#208: Fixed parsed_versions, it now honors post-releases as noted in the documentation\n* Issue \\#207: Windows cli and gui wrappers pass CTRL-C to child python process\n* Issue \\#227: easy_install now passes its arguments to setup.py bdist_egg\n* Issue \\#225: Fixed a NameError on Python 2.5, 2.4\n\n------\n0.6.21\n------\n\n* Issue \\#225: FIxed a regression on py2.4\n\n------\n0.6.20\n------\n\n* Issue \\#135: Include url in warning when processing URLs in package_index.\n* Issue \\#212: Fix issue where easy_instal fails on Python 3 on windows installer.\n* Issue \\#213: Fix typo in documentation.\n\n------\n0.6.19\n------\n\n* Issue 206: AttributeError: \'HTTPMessage\' object has no attribute \'getheaders\'\n\n------\n0.6.18\n------\n\n* Issue 210: Fixed a regression introduced by Issue 204 fix.\n\n------\n0.6.17\n------\n\n* Support \'DISTRIBUTE_DISABLE_VERSIONED_EASY_INSTALL_SCRIPT\' environment\n  variable to allow to disable installation of easy_install-${version} script.\n* Support Python >=3.1.4 and >=3.2.1.\n* Issue 204: Don\'t try to import the parent of a namespace package in\n  declare_namespace\n* Issue 196: Tolerate responses with multiple Content-Length headers\n* Issue 205: Sandboxing doesn\'t preserve working_set. Leads to setup_requires\n  problems.\n\n------\n0.6.16\n------\n\n* Builds sdist gztar even on Windows (avoiding Issue 193).\n* Issue 192: Fixed metadata omitted on Windows when package_dir\n  specified with forward-slash.\n* Issue 195: Cython build support.\n* Issue 200: Issues with recognizing 64-bit packages on Windows.\n\n------\n0.6.15\n------\n\n* Fixed typo in bdist_egg\n* Several issues under Python 3 has been solved.\n* Issue 146: Fixed missing DLL files after easy_install of windows exe package.\n\n------\n0.6.14\n------\n\n* Issue 170: Fixed unittest failure. Thanks to Toshio.\n* Issue 171: Fixed race condition in unittests cause deadlocks in test suite.\n* Issue 143: Fixed a lookup issue with easy_install.\n  Thanks to David and Zooko.\n* Issue 174: Fixed the edit mode when its used with setuptools itself\n\n------\n0.6.13\n------\n\n* Issue 160: 2.7 gives ValueError("Invalid IPv6 URL")\n* Issue 150: Fixed using ~/.local even in a --no-site-packages virtualenv\n* Issue 163: scan index links before external links, and don\'t use the md5 when\n  comparing two distributions\n\n------\n0.6.12\n------\n\n* Issue 149: Fixed various failures on 2.3/2.4\n\n------\n0.6.11\n------\n\n* Found another case of SandboxViolation - fixed\n* Issue 15 and 48: Introduced a socket timeout of 15 seconds on url openings\n* Added indexsidebar.html into MANIFEST.in\n* Issue 108: Fixed TypeError with Python3.1\n* Issue 121: Fixed --help install command trying to actually install.\n* Issue 112: Added an os.makedirs so that Tarek\'s solution will work.\n* Issue 133: Added --no-find-links to easy_install\n* Added easy_install --user\n* Issue 100: Fixed develop --user not taking \'.\' in PYTHONPATH into account\n* Issue 134: removed spurious UserWarnings. Patch by VanLindberg\n* Issue 138: cant_write_to_target error when setup_requires is used.\n* Issue 147: respect the sys.dont_write_bytecode flag\n\n------\n0.6.10\n------\n\n* Reverted change made for the DistributionNotFound exception because\n  zc.buildout uses the exception message to get the name of the\n  distribution.\n\n-----\n0.6.9\n-----\n\n* Issue 90: unknown setuptools version can be added in the working set\n* Issue 87: setupt.py doesn\'t try to convert distribute_setup.py anymore\n  Initial Patch by arfrever.\n* Issue 89: added a side bar with a download link to the doc.\n* Issue 86: fixed missing sentence in pkg_resources doc.\n* Added a nicer error message when a DistributionNotFound is raised.\n* Issue 80: test_develop now works with Python 3.1\n* Issue 93: upload_docs now works if there is an empty sub-directory.\n* Issue 70: exec bit on non-exec files\n* Issue 99: now the standalone easy_install command doesn\'t uses a\n  "setup.cfg" if any exists in the working directory. It will use it\n  only if triggered by ``install_requires`` from a setup.py call\n  (install, develop, etc).\n* Issue 101: Allowing ``os.devnull`` in Sandbox\n* Issue 92: Fixed the "no eggs" found error with MacPort\n  (platform.mac_ver() fails)\n* Issue 103: test_get_script_header_jython_workaround not run\n  anymore under py3 with C or POSIX local. Contributed by Arfrever.\n* Issue 104: remvoved the assertion when the installation fails,\n  with a nicer message for the end user.\n* Issue 100: making sure there\'s no SandboxViolation when\n  the setup script patches setuptools.\n\n-----\n0.6.8\n-----\n\n* Added "check_packages" in dist. (added in Setuptools 0.6c11)\n* Fixed the DONT_PATCH_SETUPTOOLS state.\n\n-----\n0.6.7\n-----\n\n* Issue 58: Added --user support to the develop command\n* Issue 11: Generated scripts now wrap their call to the script entry point\n  in the standard "if name == \'main\'"\n* Added the \'DONT_PATCH_SETUPTOOLS\' environment variable, so virtualenv\n  can drive an installation that doesn\'t patch a global setuptools.\n* Reviewed unladen-swallow specific change from\n  http://code.google.com/p/unladen-swallow/source/detail?spec=svn875&r=719\n  and determined that it no longer applies. Distribute should work fine with\n  Unladen Swallow 2009Q3.\n* Issue 21: Allow PackageIndex.open_url to gracefully handle all cases of a\n  httplib.HTTPException instead of just InvalidURL and BadStatusLine.\n* Removed virtual-python.py from this distribution and updated documentation\n  to point to the actively maintained virtualenv instead.\n* Issue 64: use_setuptools no longer rebuilds the distribute egg every\n  time it is run\n* use_setuptools now properly respects the requested version\n* use_setuptools will no longer try to import a distribute egg for the\n  wrong Python version\n* Issue 74: no_fake should be True by default.\n* Issue 72: avoid a bootstrapping issue with easy_install -U\n\n-----\n0.6.6\n-----\n\n* Unified the bootstrap file so it works on both py2.x and py3k without 2to3\n  (patch by Holger Krekel)\n\n-----\n0.6.5\n-----\n\n* Issue 65: cli.exe and gui.exe are now generated at build time,\n  depending on the platform in use.\n\n* Issue 67: Fixed doc typo (PEP 381/382)\n\n* Distribute no longer shadows setuptools if we require a 0.7-series\n  setuptools.  And an error is raised when installing a 0.7 setuptools with\n  distribute.\n\n* When run from within buildout, no attempt is made to modify an existing\n  setuptools egg, whether in a shared egg directory or a system setuptools.\n\n* Fixed a hole in sandboxing allowing builtin file to write outside of\n  the sandbox.\n\n-----\n0.6.4\n-----\n\n* Added the generation of `distribute_setup_3k.py` during the release.\n  This close http://bitbucket.org/tarek/distribute/issue/52.\n\n* Added an upload_docs command to easily upload project documentation to\n  PyPI\'s http://packages.python.org.\n  This close http://bitbucket.org/tarek/distribute/issue/56.\n\n* Fixed a bootstrap bug on the use_setuptools() API.\n\n-----\n0.6.3\n-----\n\nsetuptools\n==========\n\n* Fixed a bunch of calls to file() that caused crashes on Python 3.\n\nbootstrapping\n=============\n\n* Fixed a bug in sorting that caused bootstrap to fail on Python 3.\n\n-----\n0.6.2\n-----\n\nsetuptools\n==========\n\n* Added Python 3 support; see docs/python3.txt.\n  This closes http://bugs.python.org/setuptools/issue39.\n\n* Added option to run 2to3 automatically when installing on Python 3.\n  This closes http://bitbucket.org/tarek/distribute/issue/31.\n\n* Fixed invalid usage of requirement.parse, that broke develop -d.\n  This closes http://bugs.python.org/setuptools/issue44.\n\n* Fixed script launcher for 64-bit Windows.\n  This closes http://bugs.python.org/setuptools/issue2.\n\n* KeyError when compiling extensions.\n  This closes http://bugs.python.org/setuptools/issue41.\n\nbootstrapping\n=============\n\n* Fixed bootstrap not working on Windows.\n  This closes http://bitbucket.org/tarek/distribute/issue/49.\n\n* Fixed 2.6 dependencies.\n  This closes http://bitbucket.org/tarek/distribute/issue/50.\n\n* Make sure setuptools is patched when running through easy_install\n  This closes http://bugs.python.org/setuptools/issue40.\n\n-----\n0.6.1\n-----\n\nsetuptools\n==========\n\n* package_index.urlopen now catches BadStatusLine and malformed url errors.\n  This closes http://bitbucket.org/tarek/distribute/issue/16 and\n  http://bitbucket.org/tarek/distribute/issue/18.\n\n* zip_ok is now False by default. This closes\n  http://bugs.python.org/setuptools/issue33.\n\n* Fixed invalid URL error catching. http://bugs.python.org/setuptools/issue20.\n\n* Fixed invalid bootstraping with easy_install installation\n  http://bitbucket.org/tarek/distribute/issue/40.\n  Thanks to Florian Schulze for the help.\n\n* Removed buildout/bootstrap.py. A new repository will create a specific\n  bootstrap.py script.\n\n\nbootstrapping\n=============\n\n* The boostrap process leave setuptools alone if detected in the system\n  and --root or --prefix is provided, but is not in the same location.\n  This closes http://bitbucket.org/tarek/distribute/issue/10.\n\n---\n0.6\n---\n\nsetuptools\n==========\n\n* Packages required at build time where not fully present at install time.\n  This closes http://bitbucket.org/tarek/distribute/issue/12.\n\n* Protected against failures in tarfile extraction. This closes\n  http://bitbucket.org/tarek/distribute/issue/10.\n\n* Made Jython api_tests.txt doctest compatible. This closes\n  http://bitbucket.org/tarek/distribute/issue/7.\n\n* sandbox.py replaced builtin type file with builtin function open. This\n  closes http://bitbucket.org/tarek/distribute/issue/6.\n\n* Immediately close all file handles. This closes\n  http://bitbucket.org/tarek/distribute/issue/3.\n\n* Added compatibility with Subversion 1.6. This references\n  http://bitbucket.org/tarek/distribute/issue/1.\n\npkg_resources\n=============\n\n* Avoid a call to /usr/bin/sw_vers on OSX and use the official platform API\n  instead. Based on a patch from ronaldoussoren. This closes\n  http://bitbucket.org/tarek/distribute/issue/5.\n\n* Fixed a SandboxViolation for mkdir that could occur in certain cases.\n  This closes http://bitbucket.org/tarek/distribute/issue/13.\n\n* Allow to find_on_path on systems with tight permissions to fail gracefully.\n  This closes http://bitbucket.org/tarek/distribute/issue/9.\n\n* Corrected inconsistency between documentation and code of add_entry.\n  This closes http://bitbucket.org/tarek/distribute/issue/8.\n\n* Immediately close all file handles. This closes\n  http://bitbucket.org/tarek/distribute/issue/3.\n\neasy_install\n============\n\n* Immediately close all file handles. This closes\n  http://bitbucket.org/tarek/distribute/issue/3.\n',
 'download_url': 'UNKNOWN',
 'executables': {},
 'extra_source_files': [],
 'flag_options': {},
 'hook_files': [],
 'libraries': {},
 'license': 'PSF or ZPL',
 'maintainer': 'The fellowship of the packaging',
 'maintainer_email': 'distutils-sig@python.org',
 'name': 'distribute',
 'path_options': {},
 'summary': 'Easily download, build, install, upgrade, and uninstall Python packages',
 'url': 'http://packages.python.org/distribute',
 'version': '0.6.27'}