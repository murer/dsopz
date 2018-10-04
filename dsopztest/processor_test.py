import unittest
import gzip
from dsopz import io
from dsopz import util
from dsopz import processor

class ProcessorTest(unittest.TestCase):

    def test_merge(self):
        self.assertEqual(list('ax15by6z'), processor.merge([
            iter('ab'),
            iter('xyz'),
            iter('1'),
            iter('56')
        ]))

if __name__ == '__main__':
    unittest.main()
