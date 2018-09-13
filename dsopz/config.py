import argparse

class Config(object):

	def __init__(self):
		self.mods = {}
		self.parser = argparse.ArgumentParser(description='DSOpz')
		self.parser.add_argument('-a', '--auth-file', default='~/.dsopz/oauth.json', help='Local auth file')
		self.subparsers = self.parser.add_subparsers(dest="subparsers", title="Command")

	def add_parser(self, name, mod):
		self.mods[name] = mod
		return self.subparsers.add_parser(name)

	def parse_args(self):
		self.args = self.parser.parse_args()
		mod = self.mods[self.args.subparsers]
		mod()

config = Config()

"""
	sub.add_argument('-d', '--dataset', required=True, help='dataset')
	sub.add_argument('-n', '--namespace', help='namespace')
	sub.add_argument('-p', '--no-prompt', dest='prompt', action='store_false', help='no prompt')
	sub.add_argument('-sl', '--single-line', dest='single_line', action='store_true', help='single line')
	sub.add_argument('-ns', '--no-summary', dest='no_summary', action='store_true', help='single line')
	sub.add_argument('-l', '--limit', help='limit', type=int)
	sub.add_argument('-s', '--seperator', help='seperator')
"""

def main():
	parser = argparse.ArgumentParser(description='DSOpz')
	subparsers = parser.add_subparsers(dest="subparsers", title="Command")
	sub = subparsers.add_parser('login')
	sub.add_argument('-s', '--scopes', nargs='+', help='scopes', default=[
		'https://www.googleapis.com/auth/cloud-platform',
		'https://www.googleapis.com/auth/datastore',
		'https://www.googleapis.com/auth/userinfo.email'
	])
	args = parser.parse_args()
	print(args)

if __name__ == '__main__':
	print(main())
