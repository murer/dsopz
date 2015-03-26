import importer
import argparse
import oauth

def remove(dataset, block, namespace=None):
	keys = []
	for ent in block:
		key = ent['key'].copy()
		key['partitionId'] = {
			'dataset': dataset,
			'namespace': namespace
		}
		keys.append(key)
	params = { 
		'mode': 'NON_TRANSACTIONAL', 
		'mutation': { 
			'delete': keys
		}
	}
	return oauth.oauth_async_req_json('POST', 
		'https://www.googleapis.com/datastore/v1beta2/datasets/%s/commit' % (dataset), 
		params)

def import_data(dataset, kinds=[], namespace=None, chunkSize=500, parallel=10):
	importer.process_data(dataset, remove, kinds, namespace, chunkSize, parallel)

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
