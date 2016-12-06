import oauth
import json
import sys
import dsutil
import argparse
import processor

def upsert(dataset, block, namespace=None):
    for ent in block:
        ent['key']['partitionId'] = {
            'projectId': dataset,
            'namespaceId': namespace
        }
    params = {
        'mode': 'NON_TRANSACTIONAL',
        'mutations': map(lambda ent: {'upsert': ent}, block)
    }
    return oauth.oauth_async_req_json('POST',
        'https://datastore.googleapis.com/v1/projects/%s:commit' % (dataset),
        params)

def remove(dataset, block, namespace=None):
    keys = []
    for ent in block:
        key = ent['key'].copy()
        key['partitionId'] = {
            'projectId': dataset,
            'namespaceId': namespace
        }
        keys.append(key)
    params = {
        'mode': 'NON_TRANSACTIONAL',
        'mutations': map(lambda key: {'delete': key}, keys)
    }
    return oauth.oauth_async_req_json('POST',
        'https://datastore.googleapis.com/v1/projects/%s:commit' % (dataset),
        params)

class BatchProcessor(processor.Processor):

    def __init__(self, dataset, kinds, namespace, operation, block_size = 500, parallel = 10):
        super(BatchProcessor, self).__init__(kinds, block_size)
        self.dataset = dataset
        self.namespace = namespace
        self.parallel = parallel
        self.ups = []
        self.operation = operation

    def consume(self, n):
        while len(self.ups) > n:
            self.ups.pop(0).resp()

    def resolve(self):
        print >> sys.stderr, self.operation.__name__, self.processed
        self.ups.append(self.operation(self.dataset, self.block, self.namespace))
        self.consume(self.parallel)

    def done(self):
        self.consume(0)

def argparse_prepare(sub):
    sub.add_argument('-d', '--dataset', required=True, help='dataset')
    sub.add_argument('-n', '--namespace', help='namespace')
    sub.add_argument('-k', '--kinds', nargs='+', help='kinds')
    sub.add_argument('-b', '--block', type=int, help='block size')
    sub.add_argument('-p', '--parallel', type=int, help='parallel')
    sub.add_argument('-o', '--operation', required=True, choices=('upsert', 'remove'), help='operation')

def argparse_exec(args):
    op = upsert
    if args.operation == 'remove':
        op = remove
    processor = BatchProcessor(args.dataset, args.kinds, args.namespace, op, block_size = args.block or 500, parallel = args.parallel or 10)
    processor.process()
