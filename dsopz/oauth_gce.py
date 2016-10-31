import http
import time
import util
import oauth_base

class Error(Exception):
	"""Exceptions"""

def login():
	oauth_base.delete_file()
	refresh_token(None)

def refresh_token(auth):
	content = http.req_json('GET',
		'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
		headers = { 'Metadata-Flavor': 'Google' })
	now = now = int(time.time())
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	content['handler'] = 'gce'
	oauth_base.write_file(content)
	print 'Logged in'

def argparse_prepare(sub):
	""" ok """

def argparse_exec(args):
	login()
