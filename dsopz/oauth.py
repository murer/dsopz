#import os

#def auth_file():
#	return os.path.expanduser('~/.dsopz/oauth.json')

#if __name__ == '__main__':
#	print(auth_file())

"""
[
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
    'https://www.googleapis.com/auth/userinfo.email'
]
"""

from dsopz.config import config

class OAuth(object):

    def login(self):
        self._scopes = config.args.scopes or [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/datastore',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
        print(config.args, self._scopes)

oauth = OAuth()

subparser = config.add_parser('login', oauth.login)
subparser.add_argument('-s', '--scopes', nargs='+', help='scopes')
subparser.add_argument('-t', '--text', action='store_true', help='text mode')

subparser = config.add_parser('login-gce', oauth.login)

subparser = config.add_parser('login-serviceaccount', oauth.login)
subparser.add_argument('-f', '--file', required=True, help='service account json file')
