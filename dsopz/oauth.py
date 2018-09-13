#import os

#def auth_file():
#	return os.path.expanduser('~/.dsopz/oauth.json')

#if __name__ == '__main__':
#	print(auth_file())



import json as JSON
from dsopz.config import config

class OAuth(object):

    def login(self):
        self._scopes = config.args.scopes or [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/datastore',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
        self._clientsecret = {
           "installed" : {
              "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
              "client_secret" : "ZXEO84nRncBfhQnaEbMPWVfe",
              "auth_provider_x509_cert_url" : "https://www.googleapis.com/oauth2/v1/certs",
              "client_id" : "977896591232-sgpgg4ma9hbi7hvlgithb49ioj3o2sqj.apps.googleusercontent.com",
              "redirect_uris" : [
                 "urn:ietf:wg:oauth:2.0:oob",
                 "http://localhost"
              ],
              "project_id" : "dsopzproj",
              "token_uri" : "https://www.googleapis.com/oauth2/v3/token"
           }
        }
        if config.args.client:
            with open(config.args.client, 'r') as f:
                self._clientsecret = JSON.loads(f.read())
        print(config.args, self._scopes, self._clientsecret)

oauth = OAuth()

subparser = config.add_parser('login', oauth.login)
subparser.add_argument('-s', '--scopes', nargs='+', help='scopes')
subparser.add_argument('-t', '--text', action='store_true', help='text mode')
subparser.add_argument('-c', '--client', help='client secret json file')
subparser = config.add_parser('login-gce', oauth.login)
subparser = config.add_parser('login-serviceaccount', oauth.login)
subparser.add_argument('-f', '--file', required=True, help='service account json file')
