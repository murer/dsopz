import http
import urllib
import urlparse
import time
import json
import webbrowser
import oauth_base
import util
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class Error(Exception):
	"""Exceptions"""

def __config():
	return {
		'client_id': '570403801115-fik4r8kkcf89d7c46mepm5keekker8jl.apps.googleusercontent.com',
		'client_secret': 'luZsJXmEfBr4iP0WoruMbZz1',
		'scopes': [
			'https://www.googleapis.com/auth/cloud-platform',
			'https://www.googleapis.com/auth/datastore',
			'https://www.googleapis.com/auth/userinfo.email'
		]
	}

def get_first_token(port, code):
	config = __config()
	content = http.req_json('POST', 'https://www.googleapis.com/oauth2/v3/token', urllib.urlencode({
		'code': code,
		'client_id': config['client_id'],
		'client_secret': config['client_secret'],
		'redirect_uri': 'http://localhost:%s/redirect_uri' % (port),
		'grant_type': 'authorization_code'
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = now = int(time.time())
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	content['handler'] = 'local'
	oauth_base.write_file(content)
	print 'Logged in'

class OAuthHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse.urlparse(self.path)
		_, port = self.server.socket.getsockname()
		params = urlparse.parse_qs(parsed.query)
		if not params.get('code'):
			print 'Error'
			print json.dumps(params, indent=True)
		else:
			get_first_token(port, params['code'][0])
		self.send_response(302)
		self.send_header('Location', 'http://github.com/murer/dsopz')
		self.send_header('Content-type','text/plain')
		self.end_headers()
		self.wfile.write("Ok")

def login():
	oauth_base.delete_file()
	config = __config()
	server = HTTPServer(('localhost', 0), OAuthHandler)
	_, port = server.socket.getsockname()
	url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.urlencode({
		'client_id': config['client_id'],
		'redirect_uri': 'http://localhost:%s/redirect_uri' % (port),
		'response_type': 'code',
		'scope': ' '.join(config['scopes']),
		'approval_prompt': 'force',
		'access_type': 'offline'
	})
	try:
		webbrowser.open(url, new=1, autoraise=True)
		server.handle_request()
	finally:
		util.close(server.socket)

def refresh_token(auth):
	config = __config()
	content = http.req_json('POST', 'https://www.googleapis.com/oauth2/v3/token', urllib.urlencode({
		'refresh_token': auth['refresh_token'],
		'client_id': config['client_id'],
		'client_secret': config['client_secret'],
		'grant_type': 'refresh_token'
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = now = int(time.time())
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	content['refresh_token'] = auth['refresh_token']
	content['handler'] = 'local'
	oauth_base.write_file(content)

def argparse_prepare(sub):
	""" ok """

def argparse_exec(args):
	login()
