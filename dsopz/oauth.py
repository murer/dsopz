#import os

#def auth_file():
#	return os.path.expanduser('~/.dsopz/oauth.json')

#if __name__ == '__main__':
#	print(auth_file())


from dsopz.config import config

_scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
    'https://www.googleapis.com/auth/userinfo.email'
]

def cmd():
    print(config.args)

subparser = config.add_parser('login', cmd)
subparser.add_argument('-s', '--scopes', nargs='+', help='scopes', default=_scopes)
subparser.add_argument('-t', '--text', action='store_true', help='text mode')

subparser = config.add_parser('login-gce', cmd)

subparser = config.add_parser('login-serviceaccount', cmd)
subparser.add_argument('-f', '--file', required=True, help='service account json file')
