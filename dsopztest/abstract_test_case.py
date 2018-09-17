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
        config.parse_args([ 'noop' ])
        """ noop """

    def tearDown(self):
        """ close """

def noop():
    return True

subparser = config.add_parser('noop', noop)
