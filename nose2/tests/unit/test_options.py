from nose2 import options
from nose2.compat import unittest


class TestMultipassOptionParser(unittest.TestCase):

    def setUp(self):
        self.p = options.MultipassOptionParser()

    def test_parser_leaves_unhandled_arguments(self):
        args, argv = self.p.parse_args(['-x', 'foo', 'bar', '--this=that'])
        self.assertEqual(argv, ['-x', 'foo', 'bar', '--this=that'])

    def test_parser_can_extract_test_names(self):
        self.p.add_argument('tests', nargs='*', default=[])
        args, argv = self.p.parse_args(['-x', 'foo', 'bar'])
        print args, argv
        self.assertEqual(argv, ['-x'])
        self.assertEqual(args.tests, ['foo', 'bar'])

    def test_parser_can_extract_config_files_then_tests(self):
        self.p.add_argument(
            '--config', '-c', nargs='?', action='append', default=[])
        args, argv = self.p.parse_args(['-x', 'foo', '-c', 'conf.cfg',
                                        'bar', '--this=that'])
        self.assertEqual(args.config, ['conf.cfg'])
        self.assertEqual(argv, ['-x', 'foo', 'bar', '--this=that'])
        self.p.add_argument('tests', nargs='*', default=[])
        args2, argv2 = self.p.parse_args(argv)
        self.assertEqual(argv2, ['-x', '--this=that'])
        self.assertEqual(args2.tests, ['foo', 'bar'])

    def test_parser_can_extract_config_files_then_options_then_tests(self):
        self.p.add_argument(
            '--config', '-c', nargs='?', action='append', default=[])
        args, argv = self.p.parse_args(['-x', 'foo', '-c', 'conf.cfg',
                                        'bar', '--this=that'])
        self.assertEqual(args.config, ['conf.cfg'])
        self.assertEqual(argv, ['-x', 'foo', 'bar', '--this=that'])
        self.p.add_argument('-x')
        self.p.add_argument('tests', nargs='*', default=[])
        args2, argv2 = self.p.parse_args(argv)
        self.assertEqual(args2.x, 'foo')
        self.assertEqual(argv2, ['--this=that'])
        self.assertEqual(args2.tests, ['bar'])
