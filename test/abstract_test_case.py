import unittest
import shutil
import os

class Error(Exception):
    """Exceptions"""

class TestCase(unittest.TestCase):

    def configure(self):
        """ noop """

    def setUp(self):
        """ noop """

    def tearDown(self):
        """ close """
