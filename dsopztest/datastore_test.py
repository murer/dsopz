import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class DatastoreTest(abstract_test_case.TestCase):

    def test_run_query_empty(self):
        result = ds.run_query('dsopzproj', '', 'select * from notfound where x = 2 and y = 1')
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        result = ds.run_query('dsopzproj', '', result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        result = ds.run_query('dsopzproj', '', result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

    def test_full(self):

        entity = ds.centity(ds.ckey(('hero', 'ana')), ds.cprop('role', 'string', 'SUPPORT'))

        ds.mutation('dsopzproj', removes = [ entity['key'] ])

        result = ds.lookup('dsopzproj', [ entity['key'] ])
        self.assertIsNone(result.get('found'))
        self.assertEqual(1, len(result['missing']))

        result = ds.run_query('dsopzproj', '', 'select * from hero')
        self.assertEqual(0, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        ds.mutation('dsopzproj', upserts = [ entity ] )

        result = ds.run_query('dsopzproj', '', 'select * from hero')
        self.assertEqual(entity, result['batch']['entityResults'][0]['entity'])
        self.assertEqual(1, len(result['batch']['entityResults']))
        #self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        loaded = ds.lookup('dsopzproj', [ entity['key'], {
            'partitionId': { 'projectId': 'dsopzproj' },
            'path': [ { 'kind': 'notfound', 'name': 'notfound' } ]
        } ])
        self.assertEqual(entity, loaded['found'][0]['entity'])
        self.assertEqual(1, len(loaded['found']))
        self.assertEqual(1, len(loaded['missing']))

        ds.commit('dsopzproj', {
            'mode': 'NON_TRANSACTIONAL',
            'mutations': [ {
                'delete': entity['key']
            } ]
        } )

    def test_run_query_cursor(self):
        ds.mutation('dsopzproj', upserts=[ ds.centity(ds.ckey(['k', 'n%s' % i])) for i in range(3) ])
        block1 = ds.run_query('dsopzproj', '', 'select __key__ from k limit 3')
        self.assertEqual(block1['batch']['endCursor'], block1['batch']['entityResults'][2]['cursor'])
        self.assertEqual(['n0', 'n1', 'n2'], [ i['entity']['key']['path'][0]['name'] for i in block1['batch']['entityResults'] ])
        query = block1['query']

        query['startCursor'] = block1['batch']['entityResults'][0]['cursor']
        self.assertEqual(['n1', 'n2' ], [
            i['entity']['key']['path'][0]['name']
            for i in ds.run_query('dsopzproj', '', query)
            ['batch']['entityResults']
        ])
        query['startCursor'] = block1['batch']['endCursor']
        self.assertEqual([ ], [
            i['entity']['key']['path'][0]['name']
            for i in ds.run_query('dsopzproj', '', query)
            ['batch']['entityResults']
        ])

    def test_stream_entity(self):
        query = 'select __key__ from k limit 2'
        result = ds.stream_entity('dsopzproj', '', query)
        self.assertEqual({ "limit": 2, "kind": [{ "name": "k" }],
            "projection": [{ "property": { "name": "__key__" }}]},
            next(result))
        self.assertEqual([],
            [ i['entity']['key']['path'][0]['name'] for i in result])

        ds.mutation('dsopzproj', upserts=[ ds.centity(ds.ckey(['k', 'n%s' % i])) for i in range(5) ])
        self.assertEqual(['n0', 'n1' ],
            [ i['entity']['key']['path'][0]['name'] for i in
            ds.run_query('dsopzproj', '', query)['batch']['entityResults']])

        result = ds.stream_entity('dsopzproj', '', query)
        self.assertEqual({ "limit": 2, "kind": [{ "name": "k" }],
            "projection": [{ "property": { "name": "__key__" }}]},
            next(result))
        self.assertEqual(['n0', 'n1', 'n2', 'n3', 'n4'],
            [ i['entity']['key']['path'][0]['name'] for i in result])

if __name__ == '__main__':
    unittest.main()
