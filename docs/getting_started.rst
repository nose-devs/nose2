Getting started with nose2
==========================

Installation
------------

The recommended way to install nose2 is with `pip`_ ::

  pip install nose2

Running tests
-------------

To run tests in a project, use the ``nose2`` script that is installed
with nose2::

  nose2

This will find and run tests in all packages in the current working
directory, and any sub-directories of the current working directory
whose names start with 'test'.

To find tests, nose2 looks for modules whose names start with
'test'. In those modules, nose2 will load tests from all
:class:`unittest.TestCase` subclasses, as well as functions whose
names start with 'test'.

.. todo ::

   ...  and other classes whose names start with 'Test'.


The ``nose2`` script supports a number of command-line options, as
well as extensive configuration via config files. For more information
see :doc:`usage` and :doc:`configuration`.

.. _pip : http://pypi.python.org/pypi/pip/1.0.2
.. _pypi : http://pypi.python.org/pypi
