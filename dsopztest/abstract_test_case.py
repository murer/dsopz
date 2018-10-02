import unittest
import shutil
import os
from dsopz.config import config
import json as JSON
from dsopztest.datastore_emulator import dsemulator
from dsopz.oauth import oauth

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def setUp(self):
        config.parse_args([ '-u', 'http://localhost:8082', '-a', './gen/auth/oauth.json', 'noop' ])
        oauth._fake()
        dsemulator.start()

    def tearDown(self):
        dsemulator.stop()

def noop():
    return True

subparser = config.add_parser('noop', noop)
