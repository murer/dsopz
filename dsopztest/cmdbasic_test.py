from dsopz import io
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
        result = io.read_all(gz=self.sb('n1.json.gz'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'query': {'kind': [{'name': 'hero'}]}
        }, result.pop(0))
        self.assertEqual(['ana', 'nova'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

        self.xe(['download', '-rgz', self.sb('n1.json.gz'), '-f', self.sb('empty.json.gz')])
        result = io.read_all(plain=self.sb('empty.json.gz'))
        self.assertIsNotNone(result[0]['query'].pop('startCursor'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'query': {'kind': [{'name': 'hero'}]}
        }, result.pop(0))
        self.assertEqual(0, len(result))

        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero', 'tassy')), ds.cprop('role', 'string', 'SUPPORT'))
        ])

        self.xe(['download', '-a', '-rgz', self.sb('n1.json.gz'), '-fgz', self.sb('n1.json.gz')])
        result = io.read_all(gz=self.sb('n1.json.gz'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'query': {'kind': [{'name': 'hero'}]}
        }, result.pop(0))
        self.assertEqual(['ana', 'nova', 'tassy'], [ent['entity']['key']['path'][0]['name'] for ent in result] )




if __name__ == '__main__':
    unittest.main()
