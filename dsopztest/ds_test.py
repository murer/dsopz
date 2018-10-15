import unittest
from dsopztest import abstract_test_case
from dsopz.ds import Entity, Key, StringProp, format, Datastore
import json as JSON

class DSTest(abstract_test_case.TestCase):

    def test_full(self):

        entity = Entity(Key('hero', 'ana'), {'role' : StringProp('SUPPORT')})
        self.assertEqual(
            {"properties": {"role": {"stringValue": "SUPPORT", "excludeFromIndexes": False}}, "key": {"path": [{"kind": "hero", "name": "ana"}]}},
            format(entity))

        ds = Datastore('any', self.id())
        print('resut', ds.put([entity]))

        print('get', ds.get(Key('hero', 'ana')))

        """
        entity = ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT'))

        ds.mutation('dsopzproj', self.id(), removes = [ entity['key'] ])

        result = ds.lookup('dsopzproj', self.id(), [ entity['key'] ])
        self.assertEqual(0, len(result))

        result = ds.run_query('dsopzproj', self.id(), 'select * from hero')
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        ds.mutation('dsopzproj', self.id(), upserts = [ entity ] )
        entity['key'].pop('partitionId')

        result = ds.run_query('dsopzproj', self.id(), 'select * from hero')
        self.assertEqual(entity, result['batch']['entityResults'][0]['entity'])
        self.assertEqual(1, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        loaded = ds.lookup('dsopzproj', self.id(), [ entity['key'], {
            'path': [ { 'kind': 'notfound', 'name': 'notfound' } ]
        } ])
        self.assertEqual(entity, loaded[0]['entity'])
        self.assertEqual(1, len(loaded))

        ds.commit('dsopzproj', self.id(), {
            'mode': 'NON_TRANSACTIONAL',
            'mutations': [ {
                'delete': entity['key']
            } ]
        } )
        """

if __name__ == '__main__':
    unittest.main()
