import unittest
from dsopz import io2 as io
from dsopztest.abstract_test_case import BaseCase
from dsopz import datastore

class IOFileTest(BaseCase):

    def test_f(self):
        with io.write(f=self.sb('test.json'), header=Header('any', self.id(), {})) as f:
            [f.write(i) for i in range(3)]
        with io.read(f=self.sb('test.json')) as f:
            self.assertEqual('x', f.header)
            self.assertEqual(['x'], [block for block in f])

    def test_fgz(self):
        with io.write(fgz=self.sb('test.json'), header=('any', self.id(), [])) as f:
            [f.write(i) for i in range(3)]
        with io.read(fgz=self.sb('test.json')) as f:
            self.assertEqual('x', f.header)
            self.assertEqual(['x'], [block for block in f])

class DSFileTest(TestCase):

    def test_f(self):
        with io.write(partition=('any', self.id())) as f:
            [f.write({'entity'}) for i in range(3)]
        with io.read(partition=('any', self.id()), gql='select * from hero') as f:
            self.assertEqual('x', f.header)
            self.assertEqual(['x'], [block for block in f])

if __name__ == '__main__':
    unittest.main()
