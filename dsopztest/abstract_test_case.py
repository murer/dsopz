import shutil
import unittest
import os
from dsopz.config import config
import json as JSON
from dsopztest.datastore_emulator import dsemulator
from dsopz.oauth import oauth
from dsopz import cmdbasic
from dsopz import util

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def xedn(self, cmd, args):
        return self.xe([cmd, '-d', 'any', '-n', self.id()] + args)

    def xe(self, args):
        args = [ '-u', 'http://localhost:8082', '-a', './gen/auth/oauth.json' ] + args
        config.parse_args(args)

    def sb(self, name, mkdirs=True):
        ret = os.path.join('target/sandbox/', self.id(), name)
        util.makedirs(os.path.dirname(ret))
        return ret

    def _clean_sandbox(self):
        p = os.path.join('target/sandbox/', self.id())
        if os.path.isdir(p):
            shutil.rmtree(p)

    def setUp(self):
        self._clean_sandbox()
        config.parse_args([ '-u', 'http://localhost:8082', '-a', './gen/auth/oauth.json', 'noop' ])
        oauth._fake()
        dsemulator.start()

    def tearDown(self):
        dsemulator.stop()

def noop():
    return True

subparser = config.add_parser('noop', noop)
