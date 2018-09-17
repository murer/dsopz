import sys
import time
import json as JSON
import os
from dsopz.config import config
from dsopz.http import req_json
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from dsopz import util
import webbrowser

class Error(Exception):
	"""Exceptions"""

class OAuthHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse(self.path)
		_, port = self.server.socket.getsockname()
		params = parse_qs(parsed.query)
		if not params.get('code'):
			print('Error')
			print(json.dumps(params, indent=True))
		else:
			oauth._resume(port, params['code'][0])
		self.send_response(302)
		self.send_header('Location', 'http://github.com/murer/dsopz')
		self.send_header('Content-type','text/plain')
		self.end_headers()
		self.wfile.write('Ok'.encode('UTF-8'))

class OAuth(object):

    def _config(self):
        self._scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/datastore',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
        if hasattr(config.args, 'scopes') and config.args.scopes:
            self._scopes = config.args.scopes
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
        if hasattr(config.args, 'client') and config.args.client:
            with open(config.args.client, 'r') as f:
                self._clientsecret = JSON.loads(f.read())
        self._auth_file = Path(os.path.expanduser(config.args.auth_file))

    def _prepare_url(self, redirect):
        return '%s?%s' % (self._clientsecret['installed']['auth_uri'],
            urlencode({
                'client_id': self._clientsecret['installed']['client_id'],
                'redirect_uri': redirect,
                'scope': ' '.join(self._scopes),
                'response_type': 'code',
                'approval_prompt': 'force',
                'access_type': 'offline'
            }))

    def _read_file(self):
        with open(str(self._auth_file), 'r') as f:
            return JSON.loads(f.read())

    def _write_file(self, content):
        print('xxxx', self._auth_file.parent)
        util.makedirs(self._auth_file.parent)
        with open(str(self._auth_file), 'w') as f:
            f.write(JSON.dumps(content))
        print('Logged in', content)

    def _exchange_code(self, code, redirect):
        resp = req_json('POST', self._clientsecret['installed']['token_uri'], {
            'code': code,
            'client_id':  self._clientsecret['installed']['client_id'],
            'client_secret':  self._clientsecret['installed']['client_secret'],
            'redirect_uri': redirect,
            'grant_type': 'authorization_code'
        }, { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
        now = now = int(time.time())
        expires_in = resp['body']['expires_in']
        resp['body']['created'] = now
        resp['body']['expires'] = now + expires_in
        return resp['body']

    def _login_text(self):
        url = self._prepare_url('urn:ietf:wg:oauth:2.0:oob')
        print(url)
        code = sys.stdin.readline().strip()
        print('code', code)
        resp = self._exchange_code(code, 'urn:ietf:wg:oauth:2.0:oob')
        resp['handler'] = 'installed'
        self._write_file(resp)

    def _login_browser(self):
        server = HTTPServer(('localhost', 0), OAuthHandler)
        _, port = server.socket.getsockname()
        url = self._prepare_url('http://localhost:%s/redirect_uri' % (port))
        try:
            webbrowser.open(url, new=1, autoraise=True)
            server.handle_request()
        finally:
            util.close(server.socket)

    def _resume(self, port, code):
        resp = self._exchange_code(code, 'http://localhost:%s/redirect_uri' % (port))
        resp['handler'] = 'browser'
        self._write_file(resp)

    def login(self):
        self._config()
        if config.args.text:
            self._login_text()
        else:
            self._login_browser()

    def token(self):
        self._config()
        content = self._read_file()
        if not content:
            raise Error('You need to login')
        now = now = int(time.time())
        if now > content['expires'] - 60:
            self._refresh_token(content)
        return content

    def access_token(self):
        return self.token()['access_token']

    def print_token(self):
        content = self.token()
        if config.args.access_token:
            print(content['access_token'])
        else:
            print(JSON.dumps(content))

oauth = OAuth()

subparser = config.add_parser('login', oauth.login)
subparser.add_argument('-s', '--scopes', nargs='+', help='scopes')
subparser.add_argument('-t', '--text', action='store_true', help='text mode')
subparser.add_argument('-c', '--client', help='client secret json file')
subparser = config.add_parser('login-gce', oauth.login)
subparser = config.add_parser('login-serviceaccount', oauth.login)
subparser.add_argument('-f', '--file', required=True, help='service account json file')
subparser = config.add_parser('token', oauth.print_token)
subparser.add_argument('-a', '--access_token', action='store_true', help='complete json')
