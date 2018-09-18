import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class TestCase(abstract_test_case.TestCase):

    def test_run_query(self):
        result = ds.run_query('dsopzproj', '', 'select * from notfound where x = 2 and y = 1')
        self.assertEqual(0, len(result['batch']['entityResults']))
        self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

        result = ds.run_query('dsopzproj', '', result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])
        
        result = ds.run_query('dsopzproj', '', result['query'])
        self.assertEqual(0, len(result['batch']['entityResults']))
        self.assertEqual('NO_MORE_RESULTS', result['batch']['moreResults'])
        self.assertIsNotNone(result['batch']['endCursor'])

if __name__ == '__main__':
    unittest.main()
