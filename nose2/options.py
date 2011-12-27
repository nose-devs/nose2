import argparse


class MultipassOptionParser(argparse.ArgumentParser):
    """Option parser that passes through unknown arguments.

    """
    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        return args, argv
