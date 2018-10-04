import unittest
import gzip
from dsopz import io
from dsopz import util
from dsopz import processor

class ProcessorTest(unittest.TestCase):

    def test_merge_gens(self):
        self.assertEqual([
            (0, 'a'),
            (1, 'x'),
            (2, '1'),
            (3, '5'),
            (0, 'b'),
            (1, 'y'),
            (3, '6'),
            (1, 'z')
        ], [x for x in processor.merge_gens([
            iter('ab'),
            iter('xyz'),
            iter('1'),
            iter('56')
        ]) ])

    def test_abc(self):
        self.assertEqual(
            [ 'a', 'b', 'c', 'd', 'e', 'f', 'g' ],
            [x for x in processor.abc(iter('abcdefg'), maxsize=3)]
        )

if __name__ == '__main__':
    unittest.main()
