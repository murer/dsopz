import json
import util
import os

def auth_file():
	directory = os.path.expanduser('~')
	if directory == '/':
		directory = '.'
	return directory + '/.dsopz/auth.json'

def delete_file():
	try:
		os.remove(auth_file())
	except OSError:
		pass

def write_file(content):
	c = json.dumps(content, indent=True)
	name = auth_file()
	util.makedirs(os.path.dirname(name))
	with open(name, 'w') as f:
		f.write(c + '\n')

def read_file():
	if not os.path.isfile(auth_file()):
		return None 
	with open(auth_file(), 'r') as f:
		c = f.read()
	return json.loads(c)
