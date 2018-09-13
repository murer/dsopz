import reader
import argparse
import sys

class Error(Exception):
	"""Exceptions"""

def load(dataset, namespace=None):
	max_kinds = 1000
	results = reader.query(dataset, 'select __key__ from __kind__ order by __key__', namespace = namespace, limit = max_kinds)
	l = len(results['entities'])
	if l >= max_kinds:
		raise Error('Too many kinds: %i' % (max_kinds))
	ret = []
	for ent in results['entities']:
		path = ent['key']['path']
		name = path[0]['name']
		if not name.startswith('_'):
			ret.append(name)
	return ret

def argparse_prepare(sub):
	sub.add_argument('-d', '--dataset', required=True, help='dataset (pojectname)')
	sub.add_argument('-n', '--namespace', help='namespace (default: datastore default namespace)')
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds (default: all kinds)')

def argparse_exec(args):
	kinds = load(args.dataset, args.namespace)
	for kind in kinds:
		print >> sys.stdout, kind
