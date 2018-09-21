import unittest

def key(k, dataset='dsopzproj', namespace=None):
    ret = {
        'partitionId': { 'projectId': dataset },
        'path': [ { 'kind': k[0], 'name': k[1] }]
    }
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

if __name__ == '__main__':
    unittest.main()
