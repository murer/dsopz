import http
import time
import util
import oauth_base
import base64
import json
import urllib

class Error(Exception):
	"""Exceptions"""

def __config():
	return {
		'scopes': [
			'https://www.googleapis.com/auth/cloud-platform',
			'https://www.googleapis.com/auth/datastore',
			'https://www.googleapis.com/auth/userinfo.email'
		]
	}

def login(credential):
	oauth_base.delete_file()

	try:
		from Crypto.Hash import SHA256
		from Crypto.PublicKey import RSA
		from Crypto.Signature import PKCS1_v1_5
	except ImportError:
		raise Error('Service account authentication requires pycrypto')

	privatekey = RSA.importKey(credential['private_key'])
	config = __config()
	now = int(time.time())
	header = base64.urlsafe_b64encode(json.dumps({
		'alg': 'RS256',
		'typ': 'JWT',
		'kid': credential['private_key_id']
	}).encode('UTF-8'))
	payload = base64.urlsafe_b64encode(json.dumps({
		'iss': credential['client_email'],
		'scope': ' '.join(config['scopes']),
		'aud': credential['token_uri'],
		'exp': (now + 3600),
		'iat': now
	}).encode('UTF-8'))
	token = '%s.%s' % (header, payload)
	sign = token.encode('UTF-8')
	sign = PKCS1_v1_5.new(privatekey).sign(SHA256.new(sign))
	sign = base64.urlsafe_b64encode(sign)
	assertion = '%s.%s' % (token, sign)
	auth = {
		'handler': 'serviceaccount',
		'assertion': assertion,
		'token_uri': credential['token_uri']
	}
	refresh_token(auth)
	print 'Logged in'

def refresh_token(auth):
	content = http.req_json('POST', auth['token_uri'], urllib.urlencode({
		'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
		'assertion': auth['assertion']
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = int(time.time())
	expires_in = content['expires_in']
	content['created'] = now
	content['expires'] = now + expires_in
	content['assertion'] = auth['assertion']
	content['handler'] = 'serviceaccount'
	oauth_base.write_file(content)

def argparse_prepare(sub):
	sub.add_argument('-f', '--file', required=True, help='service account json file')

def argparse_exec(args):
	with open(args.file, 'r') as f:
		content = f.read()
	credential = json.loads(content)
	login(credential)
