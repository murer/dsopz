import http
import os
import urllib
import sys
import datetime
import json

class Error(Exception):
	"""Exceptions"""

def __config():
	return { 
		'client_id': '765762103246-g936peorj64mgveoqhai6ohv4t5qc5qb.apps.googleusercontent.com',
		'client_secret': 'ayQpUnTqvIxgV1XY9e-ItyC8',
		'scopes': [
			'https://www.googleapis.com/auth/cloud-platform',
			'https://www.googleapis.com/auth/datastore',
			'https://www.googleapis.com/auth/userinfo.email'
		]
	}

def __auth_file():
	directory = os.path.expanduser('~')
	if directory == '/':
		directory = '.'
	return directory + '/.dsopz/auth.json'

def __delete_file():
	try:
		os.remove(__auth_file())
	except OSError:
		pass

def __write_file(content):
	c = json.dumps(content, indent=True)
	with open(__auth_file(), 'w') as f:
		f.write(c + '\n')

def __read_file():
	if not os.path.isfile(__auth_file()):
		return None 
	with open(__auth_file(), 'r') as f:
		c = f.read()
	return json.loads(c)

def login():
	__delete_file()
	config = __config()
	url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.urlencode({
		'client_id': config['client_id'],
		'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
		'response_type': 'code',
		'scope': ' '.join(config['scopes']),
		'approval_prompt': 'force',
		'access_type': 'offline'
	})
	print 'Browser:'
	print url
	print 'Code:'
	code = sys.stdin.readline().strip()
	content = http.req_json('POST', 'https://www.googleapis.com:443/oauth2/v3/token', urllib.urlencode({
		'code': code,
		'client_id': config['client_id'],
		'client_secret': config['client_secret'],
		'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
		'grant_type': 'authorization_code'
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = int(datetime.datetime.now().strftime("%s"))
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	__write_file(content)
	print 'Done'

def __refesh_token(auth):
	config = __config()
	content = http.req_json('POST', 'https://www.googleapis.com/oauth2/v3/token', urllib.urlencode({
		'refresh_token': auth['refresh_token'],
		'client_id': config['client_id'],
		'client_secret': config['client_secret'],
		'grant_type': 'refresh_token'
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = int(datetime.datetime.now().strftime("%s"))
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	content['refresh_token'] = auth['refresh_token']
	__write_file(content)

def get_token():
	auth = __read_file()
	if not auth:
		raise Error('You need to login')
	now = int(datetime.datetime.now().strftime("%s"))
	if now > auth['expires'] - 60:
		__refesh_token(auth)
	auth = __read_file()
	if not auth:
		raise Error('You need to login')
	return auth['access_token']

def __main():
	print login()

if __name__ == '__main__':
	__main()