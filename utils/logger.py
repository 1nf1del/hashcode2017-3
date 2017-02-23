import sys


class Logger:

    def __init__(self, debug):
        self.debug = debug

    def log(self, msg):
        if self.debug:
            print(msg, file=sys.stderr)
