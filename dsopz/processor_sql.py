import argparse
import processor
import csv
import sys
import dsutil
import locale

class SQLProcessor(processor.Processor):

	def __init__(self, columns, kinds = []):
		super(SQLProcessor, self).__init__(kinds)
		self.columns = columns
		self.sql = 'insert into %s (';
		self.sql += ', '.join(['id' if str(x) == '__key__' else str(x) for x in columns])
		self.sql += ') values ('
		self.sql += ', '.join(['%s' for x in columns])
		self.sql += ');'

	def resolve(self):
		print >> sys.stderr, 'process', self.processed
		for ent in self.block:
			kind = dsutil.get_kind(ent)
			line = [ ]
			for column in self.columns:
				name  = column
				value, t = dsutil.prop_value(ent, column)
				if column == '__key__':
					name = 'id'
					last = value[len(value) - 1]
					value = last.get('name') or last.get('id')
				if t == 'booleanValue':
					value = 'TRUE' if value else 'FALSE'
				elif value:
					value = value.encode('UTF-8').replace("'", "''")
					value = "'%s'" % (value)
				line.append(value)
			values = [ kind ] + line
			print self.sql % tuple(values)

def argparse_prepare(sub):
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds')
	sub.add_argument('-c', '--columns', required=True, nargs='+', help='columns')

def argparse_exec(args):
	processor = SQLProcessor(args.columns, args.kinds)
	processor.process()
