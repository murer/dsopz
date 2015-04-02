import argparse
import sys

class Console(object):

	def __init__(self, dataset, namespace=None, prompt=True, limit=20,source=sys.stdin, dest=sys.stdout):
		self.dataset = dataset
		self.namespace = namespace
		self.prompt = prompt
		self.limit = limit
		self.source = source
		self.dest = dest

	def process(self, line):
		print >> self.dest, line

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
