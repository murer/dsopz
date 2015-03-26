import oauth
import json
import sys
import argparse

def upload(dataset, block, namespace=None):
	for ent in block:
		ent['key']['partitionId'] = {
			'dataset': dataset,
			'namespace': namespace
		}
	params = { 
		'mode': 'NON_TRANSACTIONAL', 
		'mutation': { 
			'upsert': block
		}
	}
	return oauth.oauth_async_req_json('POST', 
		'https://www.googleapis.com/datastore/v1beta2/datasets/%s/commit' % (dataset), 
		params)

def get_kind(obj):
	path = obj['key']['path']
	i = len(path)
	last = path[i - 1]
	return last['kind']

def process_data(dataset, op, kinds=[], namespace=None, chunkSize=500, parallel=10):
	kinds = kinds or []
	kinds = [k.lower() for k in kinds]
	block = []
	ups = []
	count = 0
	while True:
		line = sys.stdin.readline()
		if not line:
			break
		line = line.strip()
		if not line or line.startswith('#'):
			continue
		obj = json.loads(line)
		kind = get_kind(obj)
		if kinds and kind.lower() not in kinds:
			continue
		block.append(obj)
		if len(block) >= chunkSize:
			count += len(block)
			print >> sys.stderr, 'Uploading', count
			ups.append(op(dataset, block, namespace))
			block = []
			while len(ups) >= parallel:
				ups.pop(0).resp()
	if block:
		count += len(block)
		print >> sys.stderr, 'Uploading', count
		ups.append(op(dataset, block, namespace))
	while len(ups):
		ups.pop(0).resp()

def import_data(dataset, kinds=[], namespace=None, chunkSize=500, parallel=10):
	process_data(dataset, upload, kinds, namespace, chunkSize, parallel)

def __main():
	parser = argparse.ArgumentParser(description='Importer')
	parser.add_argument('-d', '--dataset', required=True, help='dataset')
	parser.add_argument('-n', '--namespace', required=True, help='namespace')
	parser.add_argument('-k', '--kinds', nargs='+', help='kinds')
	parser.add_argument('-p', '--parallel', type=int, help='parallel')
	args = parser.parse_args()
	import_data(args.dataset, args.kinds, args.namespace, parallel = args.parallel or 10)

if __name__ == '__main__':
	__main()
