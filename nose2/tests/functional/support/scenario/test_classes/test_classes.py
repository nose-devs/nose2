class Test(object):
    def test(self):
        pass

    def test_gen(self):
        def check(a):
            pass
        for i in range(0, 5):
            yield check, i
