import unittest
import shutil
import os
from dsopz.config import config
from dsopztest.datastore_emulator import DSEmulator

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def configure(self):
        """ noop """

    def setUp(self):
        config.parse_args([ '-u', 'http://localhost:8082', 'noop' ])
        self.server = DSEmulator()
        self.server.start()

    def tearDown(self):
        self.server.shutdown()

def noop():
    return True

subparser = config.add_parser('noop', noop)
