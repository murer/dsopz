import argparse
import processor
import sys
import json
import os

def emit(*ents):
	for ent in ents:
		if type(ent) != type([]):
			ent = [ent]
		for k in ent:
			print json.dumps(k)

class ProcessorMapper(processor.Processor):

	def __init__(self, mapper, kinds = []):
		super(ProcessorMapper, self).__init__(kinds)
		self.mapper = mapper

	def resolve(self):
		print >> sys.stderr, 'process', self.processed
		for ent in self.block:
			exec(self.mapper)

def argparse_prepare(sub):
	sub.add_argument('-k', '--kinds', nargs='+', help='kinds')

def argparse_exec(args):
	try:
		with os.fdopen(3, 'r') as f:
			mapper = f.read()
	except OSError as e:
		print >> sys.stderr, 'Try 3<map.py'
		return sys.exit(1)
	processor = ProcessorMapper(mapper, args.kinds)
	processor.process()


