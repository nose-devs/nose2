===================================
Mapping exceptions to test outcomes
===================================

.. code-block :: ini

   [outcomes]
   always-on = True
   treat-as-fail = TodoException
                   NotImplemented

.. autoplugin :: nose2.plugins.outcomes.Outcomes

