import unittest

class Layer(object):

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        raise RuntimeError('Bad Error in Layer testTearDown!')

class Test(unittest.TestCase):
    layer = Layer
    
    def testPass(self):
        pass
