import sys
from nose2.tests._common import FunctionalTestCase, support_file

try:
    import pkg_resources

except ImportError:
    pkg_resources = None

else:
    class EggDiscoveryFunctionalTest(FunctionalTestCase):
        def setUp(self):
            for m in [m for m in sys.modules if m.startswith('pkg1')]:
                del sys.modules[m]
            self.egg_path = support_file('scenario/tests_in_zipped_eggs/pkg1-0.0.0-py2.7.egg')
            for dist in pkg_resources.find_distributions(self.egg_path, only=True):
                pkg_resources.working_set.add(dist, self.egg_path)
    
        def tearDown(self):
            sys.path.remove(self.egg_path)
            for m in [m for m in sys.modules if m.startswith('pkg1')]:
                del sys.modules[m]
                
        def test_can_discover_test_modules_in_zipped_eggs(self):
            proc = self.runIn(
                'scenario/tests_in_zipped_eggs',
                '-v',
                '--plugin=nose2.plugins.loader.eggdiscovery',
                'pkg1')
            self.assertTestRunOutputMatches(proc, stderr='FAILED \(failures=5, errors=1, skipped=1\)')
    

