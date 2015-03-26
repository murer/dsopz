import argparse
import processor
import csv
import sys
import dsutil

class CSVProcessor(processor.Processor):

	def __init__(self, columns, kinds = []):
		super(CSVProcessor, self).__init__(kinds)
		self.columns = columns
		l = []
		for k in self.columns:
			if k == '__key__':
				k = 'key'
			l.append(k)
		self.writer = csv.DictWriter(sys.stdout, l, dialect='excel')
		self.writer.writeheader()

	def resolve(self):
		for ent in self.block:
			line = {}
			for column in self.columns:
				name  = column
				value, t = dsutil.prop_value(ent, column)
				if column == '__key__':
					name = 'key'
					last = value[len(value) - 1]
					value = last.get('name') or last.get('id')
				line[name] = value.encode('UTF-8')
			print line
			self.writer.writerow(line)

def __main():
	parser = argparse.ArgumentParser(description='CSV')
	parser.add_argument('-k', '--kinds', nargs='+', help='kinds')
	parser.add_argument('-c', '--columns', required=True, nargs='+', help='columns')
	args = parser.parse_args()
	processor = CSVProcessor(args.columns, args.kinds)
	processor.process()

if __name__ == '__main__':
	__main()
