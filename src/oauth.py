import oauth_local
import oauth_installed
import oauth_gce
import sys
import datetime
import http
import json
import oauth_base

class Error(Exception):
	"""Exceptions"""

def resolve(t):
	if t == 'installed':
		return oauth_installed
	elif t == 'local':
		return oauth_local
	elif t == 'gce':
		return oauth_gce
	raise Error('Unknown: %s' % (t))

def get_token():
	auth = oauth_base.read_file()
	if not auth:
		raise Error('You need to login')
	now = int(datetime.datetime.now().strftime("%s"))
	handler = resolve(auth['handler'])
	if now > auth['expires'] - 60:
		handler.refresh_token(auth)
	auth = oauth_base.read_file()
	if not auth:
		raise Error('You need to login')
	return auth['access_token']

def oauth_req_json(method, url, params = None, headers = {}, expects = [200]):
	return oauth_async_req_json(method, url, params, headers, expects).resp()

def oauth_async_req_json(method, url, params = None, headers = {}, expects = [200]):
	headers['Authorization'] = 'Bearer %s' % get_token()
	if params:
		params = json.dumps(params)
		headers['Content-type'] = 'application/json; charset=UTF-8'	
	return http.async_req_json(method, url, params, headers, expects)


def argparse_prepare(sub):
	""" ok """
	
def argparse_exec(args):
	print get_token()

def __main():
	print get_token()

if __name__ == '__main__':
	__main()

