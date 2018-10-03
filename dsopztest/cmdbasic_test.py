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

    def test_upsert(self):
        self.assertEqual([None], [ ent.get('entity') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(gz=self.sb('n1.json.gz')) as f:
            f.write({'entity': ds.centity(ds.ckey(('hero', 'ana1')), ds.cprop('role', 'string', 'SUPPORT')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'nova1')), ds.cprop('role', 'string', 'STRIKER')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'tassy1')), ds.cprop('role', 'string', 'SUPPORT')) })

        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1'],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])
        self.assertEqual([{"entity": {"key": {"path": [{"kind": "hero", "name": "ana1"}]}, "properties": {"role": {"stringValue": "SUPPORT"}}}, "version": "2"}],
            ds.lookup('any', self.id(), [{'path': [{'kind': 'hero', 'name': 'ana1' }]}]))

        with io.jwriter(gz=self.sb('n1.json.gz')) as f:
            f.write({'entity': ds.centity(ds.ckey(('hero', 'ana2')), ds.cprop('role', 'string', 'SUPPORT')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'nova2')), ds.cprop('role', 'string', 'STRIKER')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'tassy2')), ds.cprop('role', 'string', 'SUPPORT')) })

        with io.jwriter(plain=self.sb('track')) as f:
            f.write(3)
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write(2)
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write(1)
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'nova2', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write(0)
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'ana2', 'nova1', 'nova2', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

if __name__ == '__main__':
    unittest.main()
