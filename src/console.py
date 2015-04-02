import argparse
import sys
import reader
import dsutil
import json

class Console(object):

	def __init__(self, dataset, namespace=None, prompt=True,source=sys.stdin, 
			dest=sys.stdout, show_size=True, seperator='\t'):
		self.dataset = dataset
		self.namespace = namespace
		self.prompt = prompt
		self.source = source
		self.dest = dest
		self.show_size = show_size
		self.seperator = seperator

	def show_entities(self, gql, result):
		for ent in result['entities']:
			key = dsutil.human_key(ent['key'])
			line = key
			for p in ent['properties']:
				v, t = dsutil.prop_value(ent, p)
				i = ent['properties'][p].get('indexed')
				t = t.replace('Value', '')
				line += '\t%s/%s/%s/%s' % (p, t, i, json.dumps(v))
			print >> self.dest, line

	def process(self, gql):
		print >> self.dest, gql
		result = reader.query(self.dataset, gql, namespace=self.namespace, limit=0)
		self.show_entities(gql, result)
		if self.show_size:
			print >> self.dest, 'Total:', len(result['entities']), result['endCursor']

	def handle(self):
		while True:
			if self.prompt:
				self.dest.write('> ')
			line = self.source.readline()
			if not line:
				return
			line = line.strip()
			if line.startswith('#') or line.startswith('--'):
				continue
			self.process(line)

def __main():
	parser = argparse.ArgumentParser(description='Reader')
	parser.add_argument('-d', '--dataset', required=True, help='dataset')
	parser.add_argument('-n', '--namespace', help='namespace')
	parser.add_argument('-p', '--no-prompt', dest='prompt', action='store_false', help='no prompt')
	args = parser.parse_args()
	c = Console(args.dataset, namespace=args.namespace, prompt=args.prompt)
	c.handle()

if __name__ == '__main__':
	__main()
