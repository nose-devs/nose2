Welcome to nose2
================

nose2 is the next generation of nicer testing for Python, based
on the plugins branch of unittest2. nose2 aims to improve on nose by:

 * providing a better plugin api
 * being easier for users to configure
 * simplifying internal interfaces and processes
 * supporting Python 2 and 3 from the same codebase, without translation
 * encourging greater community involvment in its development

In service of some those goals, some features of nose *will not* be
supported in nose2. See `differences`_ for a thorough rundown.

In time -- once unittest2 supports plugins -- nose2 should be able to
become just a collection of plugins and configuration defaults. For
now, it provides a plugin api similar to the one in the unittest2
plugins branch, and overrides various unittest2 objects.

You are witnesses at the new birth of nose, mark 2. Hope you enjoy our
new direction!

.. _differences: http://readthedocs.org/docs/nose2/en/latest/differences.html
