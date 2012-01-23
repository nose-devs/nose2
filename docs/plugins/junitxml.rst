===========================
Outputting XML Test Reports
===========================

.. autoplugin :: nose2.plugins.junitxml.JUnitXmlReporter

Sample output
-------------

The XML test report for nose2's sample scenario with tests in a package looks like this:

.. code-block :: xml

  <testsuite errors="1" failures="5" name="nose2-junit" skips="1" tests="25" time="0.004">
    <testcase classname="pkg1.test.test_things" name="test_gen:1" time="0.000141" />
    <testcase classname="pkg1.test.test_things" name="test_gen:2" time="0.000093" />
    <testcase classname="pkg1.test.test_things" name="test_gen:3" time="0.000086" />
    <testcase classname="pkg1.test.test_things" name="test_gen:4" time="0.000086" />
    <testcase classname="pkg1.test.test_things" name="test_gen:5" time="0.000087" />
    <testcase classname="pkg1.test.test_things" name="test_gen_nose_style:1" time="0.000085" />
    <testcase classname="pkg1.test.test_things" name="test_gen_nose_style:2" time="0.000090" />
    <testcase classname="pkg1.test.test_things" name="test_gen_nose_style:3" time="0.000085" />
    <testcase classname="pkg1.test.test_things" name="test_gen_nose_style:4" time="0.000087" />
    <testcase classname="pkg1.test.test_things" name="test_gen_nose_style:5" time="0.000086" />
    <testcase classname="pkg1.test.test_things" name="test_params_func:1" time="0.000093" />
    <testcase classname="pkg1.test.test_things" name="test_params_func:2" time="0.000098">
      <failure message="test failure">Traceback (most recent call last):
    File "nose2/plugins/loader/parameters.py", line 162, in func
      return obj(*argSet)
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 64, in test_params_func
      assert a == 1
  AssertionError
  </failure>
    </testcase>
    <testcase classname="pkg1.test.test_things" name="test_params_func_multi_arg:1" time="0.000094" />
    <testcase classname="pkg1.test.test_things" name="test_params_func_multi_arg:2" time="0.000089">
      <failure message="test failure">Traceback (most recent call last):
    File "nose2/plugins/loader/parameters.py", line 162, in func
      return obj(*argSet)
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 69, in test_params_func_multi_arg
      assert a == b
  AssertionError
  </failure>
    </testcase>
    <testcase classname="pkg1.test.test_things" name="test_params_func_multi_arg:3" time="0.000096" />
    <testcase classname="" name="test_fixt" time="0.000091" />
    <testcase classname="" name="test_func" time="0.000084" />
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_failed" time="0.000113">
      <failure message="test failure">Traceback (most recent call last):
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 17, in test_failed
      assert False, "I failed"
  AssertionError: I failed
  </failure>
    </testcase>
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_ok" time="0.000093" />
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_params_method:1" time="0.000099" />
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_params_method:2" time="0.000101">
      <failure message="test failure">Traceback (most recent call last):
    File "nose2/plugins/loader/parameters.py", line 144, in _method
      return method(self, *argSet)
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 29, in test_params_method
      self.assertEqual(a, 1)
  AssertionError: 2 != 1
  </failure>
    </testcase>
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_skippy" time="0.000104">
      <skipped />
    </testcase>
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_typeerr" time="0.000096">
      <error message="test failure">Traceback (most recent call last):
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 13, in test_typeerr
      raise TypeError("oops")
  TypeError: oops
  </error>
    </testcase>
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_gen_method:1" time="0.000094" />
    <testcase classname="pkg1.test.test_things.SomeTests" name="test_gen_method:2" time="0.000090">
      <failure message="test failure">Traceback (most recent call last):
    File "nose2/plugins/loader/generators.py", line 145, in method
      return func(*args)
    File "nose2/tests/functional/support/scenario/tests_in_package/pkg1/test/test_things.py", line 24, in check
      assert x == 1
  AssertionError
  </failure>
    </testcase>
  </testsuite>

