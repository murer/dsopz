import argparse
import sys
import reader
import dsutil
import json
import cmd
import re
import http
import time

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

	def show_entities(self, gql, result, fields):
		for ent in result['entities']:
			key = dsutil.human_key(ent['key'])
			line = key
			if fields[0] == '*':
				fields = []
				for k in ent['properties'].iterkeys():
					fields.append(k)
			for p in fields:
				v, t = dsutil.prop_value(ent, p)
				prop = ent['properties'].get(p)
				line += '\t'
				if prop:
					i = prop.get('indexed')
					t = t.replace('Value', '')
					line += '%s/%s/%s/%s' % (p, t, i, json.dumps(v))
			print >> self.stdout, line

	def process(self, gql, fields):
		before = epoch_time = int(time.time())
		result = reader.query(self.dataset, gql, namespace=self.namespace, limit=0)
		after = epoch_time = int(time.time())
		self.show_entities(gql, result, fields)
		if self.show_size:
			print >> self.stdout, 'Total: %s (%s seconds)' % (len(result['entities']), (after - before))

	def parse_gql(self, line):
		temp = re.sub(r'\sfrom\s.*$', '', line)
		temp = re.sub(r'\sgroup\s.*$', '', temp)
		temp = re.sub(r'\slimit\s.*$', '', temp)
		temp = re.sub(r'\soffset\s.*$', '', temp)
		temp = re.sub(r'\sorder\s.*$', '', temp)
		temp = re.sub(r'\swhere\s.*$', '', temp)
		line = line.replace(temp, 'select *')
		fields = re.split(r'[\s,]+', temp)
		return fields, line 

	def do_select(self, line):
		fields, gql = self.parse_gql(line)
		try:
			self.process(gql, fields)
		except KeyboardInterrupt:
			print >> self.stdout, 'Interrupted'
		except Exception, e:
			print self.stdout, 'Error', e

	def do_EOF(self, line):
		return self.do_exit('exit')

	def do_exit(self, line):
		return True

	def emptyline(self):
		""" ok """

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
