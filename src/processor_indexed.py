import argparse
import processor
import sys
import json

class IndexedProcessor(processor.Processor):

	def __init__(self, columns, indexed, kinds = []):
		super(IndexedProcessor, self).__init__(kinds)
		self.columns = columns
		self.indexed = indexed

	def __setIndexed(self, column, indexed):
		if column.get('indexed') == indexed:
			return False
		column['indexed'] = indexed
		return True

	def resolve(self):
		print >> sys.stderr, 'process', self.processed
		for ent in self.block:
			changed = False
			for name in self.columns:
				column = ent['properties'].get(name)
				if not column:
					continue
				if column.get('listValue'):
					for k in column['listValue']:
						if self.__setIndexed(k, self.indexed):
							changed = True
				else:
					if self.__setIndexed(column, self.indexed):
						changed = True
			if changed:
				print json.dumps(ent)

def argparse_prepare(sub):
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds')
	sub.add_argument('-c', '--columns', required=True, nargs='+', help='columns')
	sub.add_argument('-i', '--indexed', required=True, choices=('false', 'true'), help='indexed')

def argparse_exec(args):
	processor = IndexedProcessor(args.columns, args.indexed == 'true', args.kinds)
	processor.process()


