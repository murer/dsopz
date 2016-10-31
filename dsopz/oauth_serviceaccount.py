import http
import datetime
import util
import oauth_base
import base64
import json

class Error(Exception):
	"""Exceptions"""

def _sign(key, data):
	data = data.encode('UTF-8')
	data = PKCS1_v1_5.new(key).sign(SHA256.new(message))
	return base64.urlsafe_b64encode(data)

def login(credential):
	oauth_base.delete_file()

	try:
		from Crypto.Hash import SHA256
		from Crypto.PublicKey import RSA
		from Crypto.Signature import PKCS1_v1_5
	except ImportError:
		raise Error('Service account authentication requires pycrypto')

	privatekey = RSA.importKey(credential['pem'])
	header = base64.urlsafe_b64encode(json.dumps({ 'alg': 'HS256', 'typ': 'JWT' }))
	payload = base64.urlsafe_b64encode(json.dumps({ 'a': 1 }))
	token = '%s.%s' % (header, payload)
	sign = _sign(privatekey, token)
	assertion = '%s.%s' % (token, sign)
	print assertion
	auth = {
		'handler': 'serviceaccount',
		'assertion': assertion
	}
	refresh_token(auth)

def refresh_token(auth):
	content = http.req_json('POST', 'https://www.googleapis.com:443/oauth2/v4/token', urllib.urlencode({
		'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
		'assertion': auth['assertion']
	}), { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' })
	now = int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())
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
