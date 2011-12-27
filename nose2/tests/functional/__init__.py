import os

SUPPORT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'support'))

def support_file(*path_parts):
    return os.path.join(SUPPORT, *path_parts)
