import argparse
import importer
import exporter
import reader
import console
import processor_indexed
import processor_csv
import processor_update
import processor_mapper
import oauth
import oauth_gce
import oauth_installed
import oauth_local

class Parser(object):

	def __init__(self):
		self.parser = argparse.ArgumentParser(description='DSOpz')
		self.subparsers = self.parser.add_subparsers(dest="subparsers")
		self.mods = {}

	def prepare(self, name, mod):
		sub = self.subparsers.add_parser(name)
		mod.argparse_prepare(sub)
		self.mods[name] = mod

	def handle_args(self):
		args = self.parser.parse_args()
		mod = self.mods[args.subparsers]
		mod.argparse_exec(args)

def __main():
	parser = Parser()
	parser.prepare('console', console)
	parser.prepare('export', exporter)
	parser.prepare('import', importer)
	parser.prepare('gql', reader)
	parser.prepare('index', processor_indexed)
	parser.prepare('csv', processor_csv)
	parser.prepare('update', processor_update)
	parser.prepare('map', processor_mapper)
	parser.prepare('token', oauth)
	parser.prepare('login', oauth_local)	
	parser.prepare('login-text', oauth_installed)	
	parser.prepare('login-gce', oauth_gce)	
	parser.handle_args()

if __name__ == '__main__':
	__main()


