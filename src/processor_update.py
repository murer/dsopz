import argparse
import processor
import sys
import json

class UpdateProcessor(processor.Processor):

	def __init__(self, props, kinds = []):
		super(UpdateProcessor, self).__init__(kinds)
		self.props = json.loads(props)

	def resolve(self):
		print >> sys.stderr, 'process', self.processed
		for ent in self.block:
			for name,value in self.props.iteritems():
				if value.get('indexed') == None:
					value['indexed'] = False

				ent['properties'][name] = value
			print json.dumps(ent)


def __main():
	parser = argparse.ArgumentParser(description='CSV')
	parser.add_argument('-k', '--kinds', nargs='+', help='kinds')
	parser.add_argument('-p', '--properties', required=True,  help='properties')
	args = parser.parse_args()
	processor = UpdateProcessor(args.properties ,args.kinds)
	processor.process()

if __name__ == '__main__':
	__main()

