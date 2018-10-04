import unittest
import gzip
from dsopz import io
from dsopz import util
from dsopz import processor
from time import sleep

class Error(Exception):
    """Exceptions"""

class ProcessorTest(unittest.TestCase):

    def _work(self, a, b=None):
        sleep(0.02)
        if a == 'error':
            raise Error('error')
        return (a, b)

    def _work_cancel(self, future, ret):
        ret['c'] = 1
        for _ in range(20):
            sleep(0.1)
            if future.cancel_requested():
                raise Error('cancel')
        ret['c'] = 2
        return 'done'

    def test_dispatch(self):
        f = processor.dispatch(self._work, 'a', b='b')
        self.assertEqual(False, f.done())
        self.assertIsNone(f.exception())
        self.assertEqual(('a', 'b'), f.result())

        f = processor.dispatch(self._work, 'error', b='b')
        self.assertEqual(False, f.done())
        self.assertIsNotNone(f.exception())
        with self.assertRaises(Error):
            f.result()

    def test_dispatch_cancel(self):
        data = {'c': 0}
        f = processor.dispatchf(self._work_cancel, data)
        self.assertEqual(False, f.done())
        sleep(0.02)
        self.assertEqual(1, data['c'])
        f.cancel()
        self.assertIsNotNone(f.exception())
        with self.assertRaises(Error):
            f.result()
        self.assertEqual(1, data['c'])



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

    def test_async_gen(self):
        self.assertEqual(
            [ 'a', 'b', 'c', 'd', 'e', 'f', 'g' ],
            [x for x in processor.async_gen(iter('abcdefg'), maxsize=3)]
        )

if __name__ == '__main__':
    unittest.main()
