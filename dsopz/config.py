import argparse
import logging as log

log.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(module)s:%(lineno)s] %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=log.INFO)

class Config(object):

	def __init__(self):
		self.mods = {}
		self.parser = argparse.ArgumentParser(description='DSOpz')
		self.parser.add_argument('-a', '--auth-file', default='~/.dsopz/oauth.json', help='Local auth file')
		self.parser.add_argument('-u', '--url', default='https://datastore.googleapis.com/', help='URL')
		self.subparsers = self.parser.add_subparsers(dest="subparsers", title="Command")

	def add_parser(self, name, mod):
		self.mods[name] = mod
		return self.subparsers.add_parser(name)

	def parse_args(self, args=None):
		self.args = self.parser.parse_args(args)
		mod = self.mods[self.args.subparsers]
		mod()

config = Config()
