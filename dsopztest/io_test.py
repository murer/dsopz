import unittest
import gzip
from dsopz import io
from dsopz import util

class ReaderWriterTest(unittest.TestCase):

    def test_stream_read_plain(self):
        with io.Writer('target/sandbox/data.txt', False) as f:
            f.write('line1')
            f.write('line2')
        with io.Reader('target/sandbox/data.txt', False) as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

    def test_stream_read_gz(self):
        with io.Writer('target/sandbox/data.txt.gz', True) as f:
            f.write('line1')
            f.write('line2')
        with io.Reader('target/sandbox/data.txt.gz', True) as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

if __name__ == '__main__':
    unittest.main()
