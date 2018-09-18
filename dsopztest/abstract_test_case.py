import unittest
import shutil
import os
from dsopz.config import config

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def configure(self):
        """ noop """

    def setUp(self):
        config.parse_args([ '-u', 'http://localhost:8082', 'noop' ])
        """ noop """

    def tearDown(self):
        """ close """

def noop():
    return True

subparser = config.add_parser('noop', noop)
