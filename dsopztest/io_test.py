import unittest
import gzip
from dsopz import io
from dsopz import util

class ReaderWriterTest(unittest.TestCase):

    def setUp(self):
        util.makedirs('target/sandbox')
        with open('target/sandbox/data.txt', 'wb') as f:
            f.write(b'line1\nline2\n')
        with gzip.open('target/sandbox/data.txt.gz', 'wb') as f:
            f.write(b'line1\nline2\n')

    def test_stream_read_plain(self):
        with io.Writer('target/sandbox/data.txt', False) as f:
            f.write('line1')
            f.write('line2')
        with io.Reader('target/sandbox/data.txt', False) as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

    def test_stream_read_gz(self):
        with io.Reader('target/sandbox/data.txt.gz', True) as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

if __name__ == '__main__':
    unittest.main()
