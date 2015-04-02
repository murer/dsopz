import argparse
import sys
import reader
import dsutil
import json
import cmd

class Console(cmd.Cmd):

	def __init__(self, dataset, namespace=None, prompt=True,source=sys.stdin, 
			dest=sys.stdout, show_size=True, seperator='\t'):
		cmd.Cmd.__init__(self, stdin=source, stdout=dest)
		self.dataset = dataset
		self.namespace = namespace
		self.prompt = ''
		if prompt:
			self.prompt = '> '
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
			print >> self.stdout, line

	def process(self, gql):
		result = reader.query(self.dataset, gql, namespace=self.namespace, limit=0)
		self.show_entities(gql, result)
		if self.show_size:
			print >> self.stdout, 'Total:', len(result['entities']), result['endCursor']

	def do_select(self, line):
		try:
			gql = 'select ' + line
			self.process(gql)
		except:
			e = sys.exc_info()[0]
			print >> self.stdout, e

	def do_EOF(self, line):
		return self.do_exit('exit')

	def do_exit(self, line):
		return True

	def default(self, line):
		if line:
			line = line.strip()
		if not line.startswith('#') and not line.startswith('--'):
			cmd.Cmd.default(self, line)

def __main():
	parser = argparse.ArgumentParser(description='Reader')
	parser.add_argument('-d', '--dataset', required=True, help='dataset')
	parser.add_argument('-n', '--namespace', help='namespace')
	parser.add_argument('-p', '--no-prompt', dest='prompt', action='store_false', help='no prompt')
	args = parser.parse_args()
	c = Console(args.dataset, namespace=args.namespace, prompt=args.prompt)
	try:
		c.cmdloop()
	except KeyboardInterrupt:
		return


if __name__ == '__main__':
	__main()
