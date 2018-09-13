#import os

#def auth_file():
#	return os.path.expanduser('~/.dsopz/oauth.json')

#if __name__ == '__main__':
#	print(auth_file())


from dsopz.config import config

def cmd():
    print(config.args)

subparser = config.add_parser('login', cmd)
subparser.add_argument('-s', '--scopes', nargs='+', help='scopes', default=[
		'https://www.googleapis.com/auth/cloud-platform',
		'https://www.googleapis.com/auth/datastore',
		'https://www.googleapis.com/auth/userinfo.email'
	])
