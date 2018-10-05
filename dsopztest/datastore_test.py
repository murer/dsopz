import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class DatastoreTest(abstract_test_case.TestCase):

    def test_run_query_empty(self):
        result = ds.run_query('dsopzproj', self.id(), 'select * from notfound where x = 2 and y = 1')
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        result = ds.run_query('dsopzproj', self.id(), result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        result = ds.run_query('dsopzproj', self.id(), result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

    def test_full(self):

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

    def test_run_query_cursor(self):
        ds.mutation('dsopzproj', self.id(), upserts=[ ds.centity(ds.ckey(['k', 'n%s' % i])) for i in range(3) ])
        block1 = ds.run_query('dsopzproj', self.id(), 'select __key__ from k limit 3')
        self.assertEqual(block1['batch']['endCursor'], block1['batch']['entityResults'][2]['cursor'])
        self.assertEqual(['n0', 'n1', 'n2'], [ i['entity']['key']['path'][0]['name'] for i in block1['batch']['entityResults'] ])
        query = block1['query']

        query['startCursor'] = block1['batch']['entityResults'][0]['cursor']
        self.assertEqual(['n1', 'n2' ], [
            i['entity']['key']['path'][0]['name']
            for i in ds.run_query('dsopzproj', self.id(), query)
            ['batch']['entityResults']
        ])
        query['startCursor'] = block1['batch']['endCursor']
        self.assertEqual([ ], [
            i['entity']['key']['path'][0]['name']
            for i in ds.run_query('dsopzproj', self.id(), query)
            ['batch']['entityResults']
        ])

    def test_stream_entity(self):
        query = 'select __key__ from k limit 2'
        result = ds.stream_entity('dsopzproj', self.id(), query)
        self.assertEqual({ "limit": 2, "kind": [{ "name": "k" }],
            "projection": [{ "property": { "name": "__key__" }}]},
            next(result))
        self.assertEqual([],
            [ i['entity']['key']['path'][0]['name'] for i in result])

        ds.mutation('dsopzproj', self.id(), upserts=[ ds.centity(ds.ckey(['k', 'n%s' % i])) for i in range(5) ])
        self.assertEqual(['n0', 'n1' ],
            [ i['entity']['key']['path'][0]['name'] for i in
            ds.run_query('dsopzproj', self.id(), query)['batch']['entityResults']])

        result = ds.stream_entity('dsopzproj', self.id(), query)
        self.assertEqual({ "limit": 2, "kind": [{ "name": "k" }],
            "projection": [{ "property": { "name": "__key__" }}]},
            next(result))
        self.assertEqual(['n0', 'n1', 'n2', 'n3', 'n4'],
            [ i['entity']['key']['path'][0]['name'] for i in result])

    def test_retrieve_partition(self):
        entity = ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT'))
        ds.mutation('dsopzproj', self.id(), upserts = [ entity ])
        self.assertEqual([{
                'path': [{'kind': 'hero', 'name': 'ana'}]
            }], [ i['entity']['key'] for i in
            ds.run_query('dsopzproj', self.id(), 'select * from hero')['batch']['entityResults']])
        self.assertEqual([{
                'path': [{'kind': 'hero', 'name': 'ana'}]
            }], [ i['entity']['key'] for i in
            ds.lookup('dsopzproj', self.id(), [entity['key']])])



if __name__ == '__main__':
    unittest.main()
