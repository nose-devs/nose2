Session reference
=================

Session
-------

In nose2, all configuration for a test run is encapsulated in a
``Session`` instance. Plugins always have the session available as
``self.session``.

.. autoclass :: nose2.session.Session
   :members:


Config
------

Configuration values loaded from config file sections are made
available to plugins in ``Config`` instances. Plugins that set
``configSection`` will have a ``Config`` instance available as
``self.config``.

.. autoclass :: nose2.config.Config
   :members:
