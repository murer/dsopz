import unittest
from dsopz.datastore import ckey, cprop, centity

class Error(Exception):
	"""Exceptions"""

class DatagenTest(unittest.TestCase):

    def test_key(self):
        self.assertEqual({
            'partitionId': { 'projectId': 'dsopzproj' },
            'path': [ { 'kind': 'hero', 'name': 'ana' }]
        }, ckey(('hero', 'ana')))
        self.assertEqual({
            'partitionId': { 'projectId': 'x', 'namespaceId': 'y' },
            'path': [ { 'kind': 'hero', 'name': 'ana' }]
        }, ckey(('hero', 'ana'), dataset='x', namespace='y'))
        self.assertEqual({
            'partitionId': { 'projectId': 'dsopzproj' },
            'path': [ {'kind': 'x', 'name':  'y'}, { 'kind': 'hero', 'name': 'ana' }]
        }, ckey(('x', 'y', 'hero', 'ana')))

    def test_entity(self):
        self.assertEqual({
            'key': {
                'partitionId': { 'projectId': 'dsopzproj' },
                'path': [ {'kind': 'k1', 'name':  'v1'}, { 'kind': 'k2', 'name': 'v2' }]
            },
            'properties': {
                'role': { 'stringValue': 'SUPPORT' }
            }
        }, centity(
            ckey( ('k1', 'v1', 'k2', 'v2') ),
            cprop('role', 'string', 'SUPPORT')
        ))

if __name__ == '__main__':
    unittest.main()
