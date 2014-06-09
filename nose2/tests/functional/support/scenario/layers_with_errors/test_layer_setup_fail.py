import unittest

class Layer(object):

    @classmethod
    def setUp(cls):
        raise RuntimeError('Bad Error in Layer setUp!')


class Test(unittest.TestCase):
    layer = Layer
    
    def testPass(self):
        pass
