import os

HERE = os.path.abspath(os.path.dirname(__file__))

def configFile():
    return os.path.join(HERE, 'plugins.cfg')

