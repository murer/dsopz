from dsopz import io
import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class CmdbasicTest(abstract_test_case.TestCase):

    def test_query_multiple(self):
        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero1', 'ana')), ds.cprop('role', 'string', 'SUPPORT')),
            ds.centity(ds.ckey(('hero2', 'aba')), ds.cprop('role', 'string', 'STRIKER'))
        ])
        self.xedn('download', ['-g', 'select * from hero1', 'select * from hero2', '-fgz', self.sb('n1.json.gz')])
        result = io.read_all(gz=self.sb('n1.json.gz'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'queries': [{'kind': [{'name': 'hero1'}]}, {'kind': [{'name': 'hero2'}]}]
        }, result.pop(0))
        self.assertEqual(['ana', 'aba'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero1', 'tassy')), ds.cprop('role', 'string', 'SUPPORT')),
            ds.centity(ds.ckey(('hero2', 'nova')), ds.cprop('role', 'string', 'SPEC'))
        ])
        self.xe(['download', '-fgz', self.sb('n2.json.gz'), '-rgz', self.sb('n1.json.gz')])
        result = io.read_all(gz=self.sb('n2.json.gz'))
        self.assertEqual(2, len([x.pop('startCursor') for x in result[0]['queries']]))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'queries': [{'kind': [{'name': 'hero1'}]}, {'kind': [{'name': 'hero2'}]}]
        }, result.pop(0))
        self.assertEqual(['tassy', 'nova'], [ent['entity']['key']['path'][0]['name'] for ent in result] )


    def test_query(self):
        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT')),
            ds.centity(ds.ckey(('hero', 'nova')), ds.cprop('role', 'string', 'STRIKER'))
        ])

        self.xedn('download', ['-q', '{"kind": [{"name": "hero"}]}', '-fgz', self.sb('n1.json.gz')])
        result = io.read_all(gz=self.sb('n1.json.gz'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'queries': [{'kind': [{'name': 'hero'}]}]
        }, result.pop(0))
        self.assertEqual(['ana', 'nova'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

        self.xe(['download', '-rgz', self.sb('n1.json.gz'), '-f', self.sb('empty.json.gz')])
        result = io.read_all(plain=self.sb('empty.json.gz'))
        self.assertIsNotNone(result[0]['queries'][0].pop('startCursor'))
        self.assertEqual({
            'dataset': 'any',
            'namespace': self.id(),
            'queries': [{'kind': [{'name': 'hero'}]}]
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
            'queries': [{'kind': [{'name': 'hero'}]}]
        }, result.pop(0))
        self.assertEqual(['ana', 'nova', 'tassy'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

    def test_upsert(self):
        self.assertEqual([None], [ ent.get('entity') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(gz=self.sb('n1.json.gz')) as f:
            f.write({'entity': ds.centity(ds.ckey(('hero', 'ana1')), ds.cprop('role', 'string', 'SUPPORT')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'nova1')), ds.cprop('role', 'string', 'STRIKER')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'tassy1')), ds.cprop('role', 'string', 'SUPPORT')) })

        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1'],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])
        self.assertEqual({"key": {"path": [{"kind": "hero", "name": "ana1"}]}, "properties": {"role": {"stringValue": "SUPPORT"}}},
            ds.lookup('any', self.id(), [{'path': [{'kind': 'hero', 'name': 'ana1' }]}])[0]['entity'])

        self.assertEqual([{'processed': 3}], io.read_all(plain=self.sb('track')))

        with io.jwriter(gz=self.sb('n1.json.gz')) as f:
            f.write({'entity': ds.centity(ds.ckey(('hero', 'ana2')), ds.cprop('role', 'string', 'SUPPORT')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'nova2')), ds.cprop('role', 'string', 'STRIKER')) })
            f.write({'entity': ds.centity(ds.ckey(('hero', 'tassy2')), ds.cprop('role', 'string', 'SUPPORT')) })

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 3})
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 2})
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 1})
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'nova1', 'nova2', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 0})
        self.xedn('upsert', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana1', 'ana2', 'nova1', 'nova2', 'tassy1', 'tassy2' ],
            [ ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name') for ent in ds.stream_entity('any', self.id(), 'select * from hero') ])

    def test_rm(self):
        ds.mutation('any', self.id(), upserts=[
            ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT')),
            ds.centity(ds.ckey(('hero', 'nova')), ds.cprop('role', 'string', 'STRIKER')),
            ds.centity(ds.ckey(('hero', 'tassy')), ds.cprop('role', 'string', 'SUPPORT'))
        ])
        self.xedn('download', ['-g', 'select * from hero', '-fgz', self.sb('n1.json.gz')])

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 3})
        self.xedn('rm', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana', 'nova', 'tassy'], [ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name')
            for ent in ds.stream_entity('any', self.id(), 'select __key__ from hero')] )

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 2})
        self.xedn('rm', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana', 'nova'], [ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name')
            for ent in ds.stream_entity('any', self.id(), 'select __key__ from hero')] )

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 1})
        self.xedn('rm', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None, 'ana' ], [ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name')
            for ent in ds.stream_entity('any', self.id(), 'select __key__ from hero')] )

        with io.jwriter(plain=self.sb('track')) as f:
            f.write({'processed': 0})
        self.xedn('rm', ['-fgz', self.sb('n1.json.gz'), '-r', self.sb('track')])
        self.assertEqual([None], [ent.get('entity', {}).get('key', {}).get('path', [{}])[0].get('name')
            for ent in ds.stream_entity('any', self.id(), 'select __key__ from hero')] )

if __name__ == '__main__':
    unittest.main()
