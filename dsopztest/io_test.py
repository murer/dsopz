import unittest
import gzip
from dsopz import io
from dsopz import util

class ReaderWriterTest(unittest.TestCase):

    def test_stream_read_plain(self):
        with io.JWriter('target/sandbox/data.txt', False) as f:
            f.write('line1')
            f.write('line2')
        with io.jreader(plain='target/sandbox/data.txt') as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

    def test_stream_read_gz(self):
        with io.JWriter('target/sandbox/data.txt.gz', True) as f:
            f.write('line1')
            f.write('line2')
        with io.jreader(gz='target/sandbox/data.txt.gz') as f:
            lines = [l for l in f]
            self.assertEqual(['line1', 'line2'], lines)

if __name__ == '__main__':
    unittest.main()
