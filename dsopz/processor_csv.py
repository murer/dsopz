import argparse
import processor
import csv
import sys
import dsutil
import locale

class CSVProcessor(processor.Processor):

	def __init__(self, columns, kinds = []):
		super(CSVProcessor, self).__init__(kinds)
		self.columns = columns
		l = []
		for k in self.columns:
			if k == '__key__':
				k = 'key'
			l.append(k)
		self.writer = csv.DictWriter(sys.stdout, l ,delimiter=';', quoting=csv.QUOTE_ALL)
		self.writer.writeheader()

	def resolve(self):
		print >> sys.stderr, 'process', self.processed
		for ent in self.block:
			line = {}
			for column in self.columns:
				name  = column
				value, t = dsutil.prop_value(ent, column)
				if column == '__key__':
					name = 'key'
					last = value[len(value) - 1]
					value = last.get('name') or last.get('id')
				if value:
					value = str(value).encode('UTF-8')
				line[name] = value
			self.writer.writerow(line)

def argparse_prepare(sub):
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds')
	sub.add_argument('-c', '--columns', required=True, nargs='+', help='columns')

def argparse_exec(args):
	processor = CSVProcessor(args.columns, args.kinds)
	processor.process()
