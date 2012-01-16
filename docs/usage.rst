Using nose2
===========

Running Tests
-------------

nose2

Configuration Files
-------------------

unittest.cfg

Specifying Plugins to Load
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  [unittest]
  plugins = foo
            bar
            baz

  exclude-plugins = biz
                    buz


Getting Help
------------

nose2 -h

::

  usage: nose2 [-h] [-s START_DIR] [-t TOP_LEVEL_DIRECTORY] [--config [CONFIG]]
               [--no-user-config] [--no-plugins] [--verbose] [--quiet]

  optional arguments:
    -h, --help            show this help message and exit
    -s START_DIR, --start-dir START_DIR
                          Directory to start discovery ('.' default)
    -t TOP_LEVEL_DIRECTORY, --top-level-directory TOP_LEVEL_DIRECTORY,
    --project-directory TOP_LEVEL_DIRECTORY
                          Top level directory of project (defaults to start dir)
    --config [CONFIG], -c [CONFIG]
    --no-user-config
    --no-plugins
    --verbose, -v
    --quiet
