import oauth
import json
import sys
import argparse

def __parse_entity_results(resp):
	ents = resp['batch'].get('entityResults') or []
	ret = []
	for ent in ents:
		ent = ent['entity']
		copy = {
			'key': {
				'path': ent['key']['path']
			},
			'properties': {}
		}
		for k, v in ent.get('properties', {}).iteritems():
			prop = v.copy()
			prop['indexed'] = v.pop('indexed', False)
			if prop.get('listValue'):
				prop.pop('indexed')
			if v:
				copy['properties'][k] = prop
		ret.append(copy)
	return ret

def query(dataset, gql, namespace=None, limit=1000, startCursor=None):
	url = 'https://www.googleapis.com/datastore/v1beta2/datasets/%s/runQuery' % (dataset)
	queryString = '%s limit %i' % (gql, limit)
	if startCursor:
		queryString += ' offset @startCursor'
	params = {
		'partitionId': {
			'namespace': namespace
		},
		'gqlQuery': {
			'allowLiteral': True,
			'queryString': queryString
		}
	}
	if startCursor:
		params['gqlQuery']['nameArgs'] = [{ 'name': 'startCursor', 'cursor': startCursor }]
	resp = oauth.oauth_req_json('POST', url, params)
	ret = {}
	ret['entities'] = __parse_entity_results(resp)
	ret['endCursor'] = resp['batch'].get('endCursor')
	return ret

def iterate(dataset, gql, namespace=None, bulkSize=1000):
	startCursor = None
	while True:
		page = query(dataset, gql, namespace, bulkSize, startCursor)
		if not page['entities']:
			return
		startCursor = page.get('endCursor')
		for ent in page['entities']:
			yield ent


def print_iterate(dataset, gql, namespace=None, msg=''):
	it = iterate(dataset, gql, namespace)
	loaded = 0
	try:
		while True:
			loaded += 1
			if loaded % 1000 == 0:
				print >> sys.stderr, 'loaded', msg, loaded
			string = json.dumps(it.next())
			print string
	except StopIteration:
		pass
	print >> sys.stderr, 'Done', msg, loaded

def __main():
	parser = argparse.ArgumentParser(description='Reader')
	parser.add_argument('-d', '--dataset', required=True, help='dataset')
	parser.add_argument('-n', '--namespace', required=True, help='namespace')
	parser.add_argument('-q', '--gql', required=True, help='gql')
	args = parser.parse_args()
	print_iterate(args.dataset, args.gql, args.namespace)

if __name__ == '__main__':
	__main()
