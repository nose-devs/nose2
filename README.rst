.. image:: https://travis-ci.org/nose-devs/nose2.png?branch=master
    :target: https://travis-ci.org/nose-devs/nose2
    :alt: Build Status
    
.. image:: https://coveralls.io/repos/nose-devs/nose2/badge.png?branch=master
    :target: https://coveralls.io/r/nose-devs/nose2?branch=master
    :alt: Coverage Status
    
.. image:: https://landscape.io/github/nose-devs/nose2/master/landscape.png
   :target: https://landscape.io/github/nose-devs/nose2/master
   :alt: Code Health
    
.. image:: https://pypip.in/v/nose2/badge.png
    :target: https://crate.io/packages/nose2/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/nose2/badge.png
    :target: https://crate.io/packages/nose2/
    :alt: Number of PyPI downloads
    
.. image:: https://www.versioneye.com/user/projects/52037a30632bac57a00257ea/badge.png
    :target: https://www.versioneye.com/user/projects/52037a30632bac57a00257ea/
    :alt: Dependencies Status    

Welcome to nose2
================

nose2 is the next generation of nicer testing for Python, based
on the plugins branch of unittest2. nose2 aims to improve on nose by:

 * providing a better plugin api
 * being easier for users to configure
 * simplifying internal interfaces and processes
 * supporting Python 2 and 3 from the same codebase, without translation
 * encouraging greater community involvement in its development

In service of some those goals, some features of nose *will not* be
supported in nose2. See `differences`_ for a thorough rundown.

In time -- once unittest2 supports plugins -- nose2 should be able to
become just a collection of plugins and configuration defaults. For
now, it provides a plugin api similar to the one in the unittest2
plugins branch, and overrides various unittest2 objects.

You are witnesses at the new birth of nose, mark 2. Hope you enjoy our
new direction!

.. _differences: http://readthedocs.org/docs/nose2/en/latest/differences.html
