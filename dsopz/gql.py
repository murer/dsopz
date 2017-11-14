import os
import reader
import argparse
import sys
import kind_loader

class Error(Exception):
	"""Exceptions"""

def print_iterate(dataset, gql, namespace=None, startCursor=None):
	context = {}
	reader.print_iterate(dataset, gql, namespace=namespace, startCursor=startCursor, context=context)
	try:
		with os.fdopen(3, 'w') as f:
			f.write(context['cursor'])
	except OSError as e:
		print >> sys.stderr, 'Use 3>cursor.txt to get the endCursor'

def argparse_prepare(sub):
	sub.add_argument('-d', '--dataset', required=True, help='dataset')
	sub.add_argument('-n', '--namespace', help='namespace')
	sub.add_argument('-q', '--gql', required=True, help='gql')
	sub.add_argument('-sc', '--startCursor', help='startCursor')

def argparse_exec(args):
	print_iterate(args.dataset, args.gql, args.namespace, args.startCursor)
