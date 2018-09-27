import unittest
from dsopz import io
from dsopz import util

class StreamTest(unittest.TestCase):

    def setUp(self):
        util.makedirs('target/sandbox')
        with open('target/sandbox/data.txt', 'wb') as f:
            f.write(b'line1\nline2\n')
        self.f = None

    def tearDown(self):
        self.close_f()

    def close_f(self):
        util.close(self.f)
        self.f = None

    def test_stream_read(self):
        (self.f, c) = io.stream('target/sandbox/data.txt', mode='r')
        self.assertEqual('line1\nline2\n', self.f.read())
        self.assertEqual(True, c)
        self.close_f()

        (self.f, c) = io.stream('target/sandbox/data.txt', mode='r')
        lines = [l for l in self.f]
        self.assertEqual(['line1\n', 'line2\n'], lines)
        self.assertEqual(True, c)
        self.close_f()



if __name__ == '__main__':
    unittest.main()
