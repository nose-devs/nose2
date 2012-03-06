class Test(object):

    @classmethod
    def setUpClass(cls):
        cls.setup = 1

    @classmethod
    def tearDownClass(cls):
        del cls.setup

    def setUp(self):
        self.test_setup = 1

    def tearDown(self):
        del self.test_setup

    def test(self):
        assert self.test_setup
        assert self.setup

    def test_gen(self):
        def check(a):
            assert self.setup
            assert self.test_setup
        for i in range(0, 2):
            yield check, i
