import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class CmdbasicTest(abstract_test_case.TestCase):


    def test_query(self):
        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT')),
            ds.centity(ds.ckey(('hero', 'nova')), ds.cprop('role', 'string', 'STRIKER'))
        ])

        self.xedn('download', ['-q', 'select * from hero', '-fgz', self.sb('n1.json.gz')])

if __name__ == '__main__':
    unittest.main()
