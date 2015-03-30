import unittest
import src.reader as reader
import src.importer as importer
import src.exporter as exporter
import os

def config():
	return {
		"dataset": os.environ.get('DSOPZ_TEST_DATASET', 'cloudcontainerz'),
		"namespace": os.environ.get('DSOPZ_TEST_NAMESPACE', 'dsopz_test')
	}

def clean():
	config = config()
	

class TestCase(unittest.TestCase):

  def setUp(self):
    clean()

  def tearDown(self):
    clean()

class ReaderTest(TestCase):

  def test_query(self):
  	print config()


if __name__ == '__main__':
    unittest.main()
