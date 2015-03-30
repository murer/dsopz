import unittest
import src.reader as reader

class TestCase(unittest.TestCase):

  def setUp(self):
    """ setUp """

  def tearDown(self):
    """ tearDown """

class ReaderTest(TestCase):

  def test_query(self):
    print reader


if __name__ == '__main__':
    unittest.main()
