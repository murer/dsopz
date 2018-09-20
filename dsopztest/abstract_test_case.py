import unittest
import shutil
import os
from dsopz.config import config
import json as JSON
from dsopztest.datastore_emulator import DSEmulator
from dsopz.oauth import oauth

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def setUp(self):
        config.parse_args([ '-u', 'http://localhost:8082', '-a', './gen/auth/oauth.json', 'noop' ])
        oauth._config()
        oauth._write_file({
            "expires" : 1537467118,
            "access_token" : "dummytoken"
        })
        self.server = DSEmulator()
        self.server.start()

    def tearDown(self):
        self.server.shutdown()

def noop():
    return True

subparser = config.add_parser('noop', noop)
