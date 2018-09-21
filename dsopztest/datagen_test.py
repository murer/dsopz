import unittest

class Error(Exception):
	"""Exceptions"""

def key(k, dataset='dsopzproj', namespace=None):
    if len(k) % 2 != 0:
        raise Error('must be even %s' % (k))
    ret = {
        'partitionId': { 'projectId': dataset },
        'path': []
    }
    for i in range(0, len(k), 2):
        ret['path'].append({ 'kind': k[i], 'name': k[i+1] })
    if namespace:
        ret['partitionId']['namespaceId'] = namespace
    return ret

class DatagenTest(unittest.TestCase):

    def test_key(self):
        self.assertEqual({
            'partitionId': { 'projectId': 'dsopzproj' },
            'path': [ { 'kind': 'hero', 'name': 'ana' }]
        }, key(('hero', 'ana')))
        self.assertEqual({
            'partitionId': { 'projectId': 'x', 'namespaceId': 'y' },
            'path': [ { 'kind': 'hero', 'name': 'ana' }]
        }, key(('hero', 'ana'), dataset='x', namespace='y'))
        self.assertEqual({
            'partitionId': { 'projectId': 'dsopzproj' },
            'path': [ {'kind': 'x', 'name':  'y'}, { 'kind': 'hero', 'name': 'ana' }]
        }, key(('x', 'y', 'hero', 'ana')))

if __name__ == '__main__':
    unittest.main()
