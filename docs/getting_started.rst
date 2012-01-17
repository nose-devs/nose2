Getting started with nose2
==========================

Installation
------------

The recommended way to install nose2 is with `pip`_ ::

  pip install nose2

You can also install from source by downloading the source
distribution from `pypi`_, un-taring it, and running
``python setup.py install`` in the source directory. Note that if you
install this way, and do not have distribute or setuptools installed,
you must install nose2's dependencies manually.


Dependencies
~~~~~~~~~~~~

For Python 2.7, Python 3.2 and pypy, nose2 requires `six`_ version
1.1. For Python 2.6, nose2 also requires `argparse`_ version 1.2.1 and
`unittest2`_ version 0.5.1. When installing with pip, distribute or
setuptools, these dependencies will be installed automatically.


Development version
~~~~~~~~~~~~~~~~~~~

You can install the development version of nose2 from github with `pip`_::

  pip install -e git+git://github.com/nose-devs/nose2.git#egg=nose2

You can also download a package from github, or clone the source and install
from there with ``python setup.py install``.


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
.. _six : http://pypi.python.org/pypi/six/1.1.0
.. _argparse : http://pypi.python.org/pypi/argparse/1.2.1
.. _unittest2 : http://pypi.python.org/pypi/unittest2/0.5.1
