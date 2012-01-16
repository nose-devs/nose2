Hook reference
==============

Hooks
-----

.. note ::

   Hooks are listed here in order of execution. See FIXME


.. function :: pluginsLoaded(self, event)

   :param event: :class:`nose2.events.PluginsLoadedEvent`

   The ``pluginsLoaded`` hook is called after all config files have been read,
   and all plugin classes loaded. Plugins that register automatically
   (those that call :meth:`nose2.events.Plugin.register` in __init__
   or have ``always-on = True`` set in their config file sections) will
   have already been registered with the hooks they implement. Plugins
   waiting for commmand-line activation will not yet be registered.

   Plugins can use this hook to examine or modify the set of loaded plugins,
   inject their own hook methods using
   :meth:`nose2.events.PluginInterface.addMethod`, or take other
   actions to set up or configure themselves or the test run.

   Since ``pluginsLoaded`` is a pre-registration hook, it is called
   for *all plugins* that implement the method, whether they have
   registered or not. Plugins that do not automatically register
   themselves should limit their actions in this hook to
   configuration, since they may not actually be active during the
   test run.

.. function :: handleArgs(self, event)

   :param event: :class:`nose2.events.CommandLineArgsEvent`

   The ``handleArgs`` hook is called after all arguments from the command
   line have been parsed. Plugins can use this hook to handle command-line
   arguments in non-standard ways. They should not use it to try to modify
   arguments seen by other plugins, since the order in which plugins
   execute in a hook is not guaranteed.

   Since ``handleArgs`` is a pre-registration hook, it is called for
   *all plugins* that implement the method, whether they have registered
   or not. Plugins that do not automatically register
   themselves should limit their actions in this hook to
   configuration, since they may not actually be active during the
   test run.
