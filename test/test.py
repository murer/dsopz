import unittest
import src.reader as reader

class TestCase(unittest.TestCase):

  def setUp(self):
    """ setUp """

  def tearDown(self):
    """ tearDown """

class ReaderTest(TestCase):

  def test_query(self):
    reader.query('cloudcontainerz', 'select *', namespace='dsopz_test', limit=2)


if __name__ == '__main__':
    unittest.main()
