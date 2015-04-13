import argparse
import sys
import reader
import dsutil
import json
import cmd
import re
import http
import time
import sys

class Console(cmd.Cmd):

	def __init__(self, dataset, namespace=None, prompt=True,source=sys.stdin, 
			dest=sys.stdout, show_size=True, seperator='\t', double_endline=True,
			limit=None):
		cmd.Cmd.__init__(self, stdin=source, stdout=dest)
		self.dataset = dataset
		self.namespace = namespace
		self.prompt = ''
		if prompt:
			self.prompt = '> '
		self.show_size = show_size
		self.seperator = '\t'
		if seperator != None:
			self.seperator = seperator
		self.double_endline = double_endline
		self.limit = limit or 0

	def show_entities(self, gql, result, fields):
		for ent in result:
			key = dsutil.human_key(ent['key'])
			line = key
			if fields[0] == '*':
				fields = []
				for k in ent['properties'].iterkeys():
					fields.append(k)
			for p in fields:
				v, t = dsutil.prop_value(ent, p)
				prop = ent['properties'].get(p)
				line += self.seperator
				if prop:
					i = prop.get('indexed')
					t = t.replace('Value', '')
					line += '%s/%s/%s/%s' % (p, t, i, json.dumps(v))
			print >> self.stdout, line
			if self.double_endline:
				print >> self.stdout, ''

	def process(self, gql, fields):
		before = int(time.time())
		bulkSize = 1000
		if self.limit > 0:
			bulkSize = min(bulkSize, self.limit)
		it = reader.iterate(self.dataset, gql, namespace=self.namespace, bulkSize=bulkSize)
		loaded = 0
		limited = ''
		try:
			while True:
				ent = it.next()
				self.show_entities(gql, [ent], fields)
				loaded += 1
				if self.limit and loaded >= self.limit:
					limited = 'limited '
					break 
		except StopIteration:
			pass
		after = int(time.time())
		if self.show_size:
			print >> self.stdout, 'Total: %s %s(%s seconds)' % (loaded, limited, (after - before))

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
			print >> self.stdout, 'Error', e

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

def argparse_prepare(sub):
	sub.add_argument('-d', '--dataset', required=True, help='dataset')
	sub.add_argument('-n', '--namespace', help='namespace')
	sub.add_argument('-p', '--no-prompt', dest='prompt', action='store_false', help='no prompt')
	sub.add_argument('-sl', '--single-line', dest='single_line', action='store_true', help='single line')
	sub.add_argument('-ns', '--no-summary', dest='no_summary', action='store_true', help='single line')
	sub.add_argument('-l', '--limit', help='limit', type=int)
	sub.add_argument('-s', '--seperator', help='seperator')

def argparse_exec(args):
	limit = args.limit
	if limit == None:
		limit = 10
	c = Console(args.dataset, namespace=args.namespace, prompt=args.prompt, 
		double_endline=not args.single_line, show_size=not args.no_summary,
		limit=limit, seperator=args.seperator)
	try:
		c.cmdloop()
	except KeyboardInterrupt:
		return

