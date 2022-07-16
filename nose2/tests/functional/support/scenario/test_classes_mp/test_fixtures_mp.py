class Test:
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
            assert self.test_setup
            assert self.setup

        for i in range(0, 2):
            yield check, i

    def test_params(self, a):
        assert self.test_setup
        assert self.setup

    test_params.paramList = (1, 2)
