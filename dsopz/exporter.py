import reader
import argparse
import sys
import kind_loader

class Error(Exception):
	"""Exceptions"""

def print_iterate(dataset, kinds=[], namespace=None, keys_only=False):
	if not kinds:
		kinds = kind_loader.load(dataset, namespace)
	field = '*'
	if keys_only:
		field = '__key__'
	for kind in kinds:
		reader.print_iterate(dataset,
			'select %s from `%s` order by __key__' % (field, kind),
			namespace=namespace, msg=kind)

def argparse_prepare(sub):
	sub.add_argument('-d', '--dataset', required=True, help='dataset (pojectname)')
	sub.add_argument('-n', '--namespace', help='namespace (default: datastore default namespace)')
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds (default: all kinds)')
	sub.add_argument('-o', '--keys-only', help='keys only (default: false)')

def argparse_exec(args):
	print_iterate(args.dataset, args.kinds, args.namespace, args.keys_only == 'true')
