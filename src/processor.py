import argparse
import dsutil
import sys
import json

class Error(Exception):
	"""Exceptions"""

class ProcessorError(Error):
	"""Exceptions"""

class Processor(object):

	def __init__(self, kinds = [], block_size=500):
		self.kinds = kinds or []
		self.kinds = [k.lower() for k in self.kinds]
		self.block_size = block_size

	def resolve(self):
		raise ProcessorError('You need to implement process')

	def done(self):
		""" Done """

	def process(self):
		self.block = []
		self.processed = 0
		while True:
			line = sys.stdin.readline()
			if not line:
				break
			line = line.strip()
			if not line or line.startswith('#'):
				continue
			obj = json.loads(line)
			kind = dsutil.get_kind(obj)
			if self.kinds and kind.lower() not in self.kinds:
				continue
			self.block.append(obj)
			if len(self.block) >= self.block_size:
				self.processed += len(self.block)
				self.resolve()
				self.block = []
		if self.block:
			self.processed += len(self.block)
			self.resolve()
			self.block = []
		self.done()

class PrintProcessor(Processor):

	def __init__(self, columns, kinds = [], separator = '\t'):
		super(PrintProcessor, self).__init__(kinds)
		self.columns = columns
		if separator == None:
			self.separator = '\t'
		else:
			self.separator = separator.decode('string_escape')

	def resolve(self):
		for ent in self.block:
			line = ''
			for i, column in enumerate(self.columns):
				value, t = dsutil.prop_value(ent, column)
				if column == '__key__' or t == 'keyValue':
					value = dsutil.human_key(value)
				else:
					value = json.dumps(value)
				line += value
				if i < len(self.columns) - 1:
					line += self.separator
			print line

	def headers(self):
		line = ''
		for i, column in enumerate(self.columns):
			line += column
			if i < len(self.columns) - 1:
				line += self.separator
		print line

def __main():
	parser = argparse.ArgumentParser(description='Processor')
	parser.add_argument('-k', '--kinds', nargs='+', help='kinds')
	parser.add_argument('-c', '--columns', required=True, nargs='+', help='columns')
	parser.add_argument('-s', '--separator', help='separator')
	parser.add_argument('-a', '--headers', help='headers')
	args = parser.parse_args()
	processor = PrintProcessor(args.columns, args.kinds, args.separator)
	if args.headers:
		processor.headers()
	processor.process()

if __name__ == '__main__':
	__main()
