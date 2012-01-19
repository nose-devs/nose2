===============
Writing Plugins
===============

nose2 supports plugins for test collection, selection, observation and
reporting -- among other things. There are two basic rules for plugins:

* Plugin classes must subclass :class:`nose2.events.Plugin`.

* Plugins may implement any of the methods described in the
  :doc:`hook_reference`.


Hello World
===========

Here's a basic plugin. It doesn't do anything besides log a message at
the start of a test run.

.. code-block:: python

    import logging
    import os

    from nose2.events import Plugin

    log = logging.getLogger('nose2.plugins.helloworld')

    class HelloWorld(Plugin):
        configSection = 'helloworld'
        commandLineSwitch = (None, 'hello-world', 'Say hello!')

        def startTestRun(self, event):
            log.info('Hello pluginized world!')

To see this plugin in action, save it into an importable module, then
add that module to the ``plugins`` key in the ``[unittest]`` section
of a config file loaded by nose2, such as ``unittest.cfg``. Then run
nose2::

  nose2 --log-level=INFO --hello-world

And you should see the log message before the first dot appears.


Loading plugins
===============

As mentioned above, for nose2 to find a plugin, it must be in an
importable module, and the module must be listed under the ``plugins``
key in the ``[unittest]`` section of a config file loaded by nose2:

.. code-block:: ini

   [unittest]
   plugins = mypackage.someplugin
             otherpackage.thatplugin
             thirdpackage.plugins.metoo

As you can see, plugin *modules* are listed, one per line. All plugin
classes in those modules will be loaded -- but not necessarily
active. Typically plugins do not activate themselves ("register")
without seeing a command-line flag, or ``always-on = True`` in their
config file section.


Command-line Options
====================

nose2 uses `argparse`_ for command-line argument parsing. Plugins may
enable command-line options that register them as active, or take
arguments or flags controlling their operation.

The most basic thing to do is to set the plugin's
``commandLineSwitch`` attribute, which will automatically add a
command-line flag that registers the plugin.

To add other flags or arguments, you can use the Plugin methods
:meth:`nose2.events.Plugin.addFlag`,
:meth:`nose2.events.Plugin.addArgument` or
:meth:`nose2.events.Plugin.addOption`. If those don't offer enough
flexibility, you can directly manipulate the argument parser by
accessing ``self.session.argparse`` or the plugin option group by
accessing ``self.session.pluginargs``.

Please note though that the *majority* of your plugin's configuration
should be done via config file options, not command line options.


Config File Options
===================

Plugins may specify a config file section that holds their
configuration by setting their ``configSection`` attribute. All
plugins, regardless of whether they specify a config section, have a
``config`` attribute that holds a :class:`nose2.config.Config`
instance. This will be empty of values if the plugin does not specify
a config section or if no loaded config file includes that section.

Plugins should extract the user's configuration selections from their
config attribute in their ``__init__`` methods. Plugins that want to
use nose2's `Sphinx`_ extension to automatically document themselves
**must** do so.

Config file options may be extracted as strings, ints, booleans or
lists.

You should provide reasonable defaults for all config options.

Guidelines
==========

Events
------

nose2's plugin api is based on the api in unittest2's
under-development plugins branch. It differs from nose's plugins api
in one major area: what it passes to hooks. Where nose passes a
variety of arguments, nose2 *always passes an event*. The events are
listed in the :doc:`event_reference`.

Here's the key thing about that: *event attributes are
read-write*. Unless stated otherwise in the documentation for a hook,
you can set a new value for any event attribute, and *this will do
something*. Plugins and nose2 systems will see that new value and
either use it instead of what was originally set in the event
(example: the reporting stream or test executor), or use it to
supplement something they find elsewhere (example: extraTests on a
test loading event).

"Handling" events
~~~~~~~~~~~~~~~~~

Many hooks give plugins a chance to completely handle events,
bypassing other plugins and any core nose2 operations. To do this, a
plugin sets ``event.handled`` to True and, generally, returns an
appropriate value from the hook method. What is an appropriate value
varies by hook, and some hooks *can't* be handled in this way. But
even for hooks where handling the event doesn't stop all processing,
it *will* stop subsequently-loaded plugins from seeing the event.

Logging
-------

nose2 uses the logging classes from the standard library. To enable users
to view debug messages easily, plugins should use ``logging.getLogger()`` to
acquire a logger in the ``nose2.plugins`` namespace.

.. todo ::

   more guidelines

Recipes
=======

* Writing a plugin that monitors or controls test result output

  Implement any of the ``report*`` hook methods, especially if you
  want to output to the console. If outputing to file or other system,
  you might implement :func:`testOutcome` instead.

  Example: :class:`nose2.plugins.result.ResultReporter`

* Writing a plugin that handles exceptions

  If you just want to handle some exceptions as skips or failures
  instead of errors, see :class:`nose2.plugins.outcomes.Outcomes`,
  which offers a simple way to do that. Otherwise, implement
  :func:`setTestOutcome` to change test outcomes.

  Example: :class:`nose2.plugins.outcomes.Outcomes`

* Writing a plugin that adds detail to error reports

  Implement :func:`testOutcome` and put your extra information into
  ``event.metadata``, then implement :func:`outcomeDetail` to extract
  it and add it to the error report.

  Examples: :class:`nose2.plugins.buffer.OutputBufferPlugin`, :class:`nose2.plugins.logcapture.LogCapture`

* Writing a plugin that loads tests from files other than python modules

  Implement :func:`handleFile`.

  Example: :class:`nose2.plugins.doctests.DocTestLoader`

* Writing a plugin that prints a report

  Implement :func:`beforeErrorList`, :func:`beforeSummaryReport` or
  :func:`afterSummaryReport`

  Example: :class:`nose2.plugins.prof.Profiler`

* Writing a plugin that selects or rejects tests

  Implement :class:`matchPath` or :class:`getTestCaseNames`.

  Example: :class:`nose2.plugins.loader.parameters.Parameters`

.. _argparse : http://pypi.python.org/pypi/argparse/1.2.1
.. _Sphinx : http://sphinx.pocoo.org/
