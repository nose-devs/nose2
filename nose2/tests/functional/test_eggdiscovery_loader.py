import sys
from nose2.tests._common import FunctionalTestCase, support_file

try:
    import pkg_resources

except ImportError:
    pkg_resources = None

else:
    class EggDiscoveryFunctionalTest(FunctionalTestCase):
        def setUp(self):
            for m in [m for m in sys.modules if m.startswith('pkgegg')]:
                del sys.modules[m]
            self.egg_path = support_file('scenario/tests_in_zipped_eggs/pkgegg-0.0.0-py2.7.egg')
            sys.path.append(self.egg_path)
    
        def tearDown(self):
            if self.egg_path in sys.path:
                sys.path.remove(self.egg_path)
            for m in [m for m in sys.modules if m.startswith('pkgegg')]:
                del sys.modules[m]
            reload(pkg_resources)
        
        def test_non_egg_discoverer_does_not_fail_when_looking_in_egg(self):
            proc = self.runIn(
                'scenario/tests_in_zipped_eggs',
                '-v',
                'pkgegg')
            self.assertTestRunOutputMatches(proc, stderr='Ran 0 tests in')
        
        def test_can_discover_test_modules_in_zipped_eggs(self):
            proc = self.runIn(
                'scenario/tests_in_zipped_eggs',
                '-v',
                '--plugin=nose2.plugins.loader.eggdiscovery',
                'pkgegg')
            self.assertTestRunOutputMatches(proc, stderr='FAILED \(failures=5, errors=1, skipped=1\)')
    

