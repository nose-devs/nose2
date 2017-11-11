.. image:: https://travis-ci.org/nose-devs/nose2.png?branch=master
    :target: https://travis-ci.org/nose-devs/nose2
    :alt: Build Status
    
.. image:: https://coveralls.io/repos/nose-devs/nose2/badge.png?branch=master
    :target: https://coveralls.io/r/nose-devs/nose2?branch=master
    :alt: Coverage Status
    
.. image:: https://landscape.io/github/nose-devs/nose2/master/landscape.png
   :target: https://landscape.io/github/nose-devs/nose2/master
   :alt: Code Health
    
.. image:: https://img.shields.io/pypi/v/nose2.svg
    :target: https://pypi.org/project/nose2/
    :alt: Latest PyPI version

.. image:: https://www.versioneye.com/user/projects/52037a30632bac57a00257ea/badge.png
    :target: https://www.versioneye.com/user/projects/52037a30632bac57a00257ea/
    :alt: Dependencies Status    

.. image:: https://badges.gitter.im/gitterHQ/gitter.png
    :target: https://gitter.im/nose2
    :alt: Gitter Channel

Welcome to nose2
================

**Note**: As of 0.7.0 we no longer support 2.6, 3.2, or 3.3. We also removed ``nose2.compat``.

``nose2`` aims to improve on nose by:

 * providing a better plugin api
 * being easier for users to configure
 * simplifying internal interfaces and processes
 * supporting Python 2 and 3 from the same codebase, without translation
 * encouraging greater community involvement in its development

In service of some those goals, some features of ``nose`` *are not*
supported in ``nose2``. See `differences`_ for a thorough rundown.

Workflow
--------

If you want to make contributions, you can use the ``Makefile`` to get started
quickly and easily::

    # All you need is a supported version of python and virtualenv installed
    make test

tox will run our full test suite
against all supported version of python that you have installed locally.
Don't worry if you don't have all supported versions installed.
Your changes will get tested automatically when you make a PR.

Use ``make help`` to see other options.

Original Mission & Present Goals
--------------------------------

When ``nose2`` was first written, the plan for its future was to wait for
``unittest2`` plugins to be released (``nose2`` is actually based on the
plugins branch of ``unittest2``).
Once that was done, ``nose2`` was to become a set of plugins and default
configuration for ``unittest2``.

However, based on the current status of ``unittest2``, it is doubtful that this
plan will ever be carried out.

Current Goals
~~~~~~~~~~~~~

Even though ``unittest2`` plugins never arrived, ``nose2`` is still being
maintained!
We have a small community interested in continuing to work on and use ``nose2``

However, given the current climate, with much more interest accruing around
`pytest`_, ``nose2`` is prioritizing bugfixes and maintenance ahead of new
feature development.

.. _differences: https://nose2.readthedocs.io/en/latest/differences.html

.. _pytest: http://pytest.readthedocs.io/en/latest/
