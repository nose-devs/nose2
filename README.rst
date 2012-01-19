Welcome to nose2
================

.. warning ::

   This is an early, pre-alpha release of nose2. It is not
   feature-complete, and will mostly be of interest to plugin authors,
   folks who want to contribute to nose2, and testing nerds. While of
   course we want you to try it out, you should probably not use nose2
   to run the test suite for your giant robot crane.

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

.. _differences: http://nose-devs.github.com/nose2/differences.html
