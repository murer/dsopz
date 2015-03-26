import argparse
import dsutil
import sys
import json

class Error(Exception):
	"""Exceptions"""

class ProcessorError(Error):
	"""Exceptions"""

class Transformer(object):

	def __init__(self, kinds = [], block_size=2):
		self.kinds = kinds or []
		self.kinds = [k.lower() for k in self.kinds]
		self.block_size = block_size

	def process(self):
		raise ProcessorError('You need to implement process')

	def transform(self):
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
				self.process()
				self.block = []
		if block:
			self.processed += len(block)
			self.process()
			self.block = []

class PrintTransfomer(Transformer):

	def __init__(self, columns, kinds = [], separator = '\t'):
		super(PrintTransfomer, self).__init__(kinds)
		self.columns = columns
		if separator == None:
			self.separator = '\t'
		else:
			self.separator = separator.decode('string_escape')

	def process(self):
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

def __main():
	parser = argparse.ArgumentParser(description='Transformer')
	parser.add_argument('-k', '--kinds', nargs='+', help='kinds')
	parser.add_argument('-c', '--columns', required=True, nargs='+', help='columns')
	parser.add_argument('-s', '--separator', help='separator')
	args = parser.parse_args()
	transformer = PrintTransfomer(args.columns, args.kinds, args.separator)
	transformer.transform()

if __name__ == '__main__':
	__main()
