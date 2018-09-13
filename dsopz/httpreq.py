from http.client import HTTPSConnection, HTTPConnection
import json as JSON
from dsopz import util
import threading
from urllib.parse import urlparse

class Error(Exception):
	"""Exceptions"""

def req_json(method, url, params = '', headers = {}, expects = [200]):
	parsed = urlparse(url)
	host = parsed.netloc
	uri = parsed.path
	if(parsed.query != ''):
		uri = uri + '?' + parsed.query
	conn = None
	if(parsed.scheme == 'https'):
		conn = HTTPSConnection(parsed.hostname, parsed.port or 443)
	else:
		conn = HTTPConnection(parsed.hostname, parsed.port or 80)
	if parsed.username != None:
		token = parsed.username + ':' + (parsed.password or '')
		token = 'Basic ' + base64.b64encode(token)
		headers['Authorization'] = token
	try:
		conn.request(method, uri, params, headers)
		response = conn.getresponse()
		if response.status not in expects:
			raise Error('Status: %d %s %sri' % (response.status, response.reason, response.read()))
		string = response.read()
		if not string:
			return None
		ret = JSON.loads(string.decode('UTF-8'))
		return {
			'status': response.status,
			'body': ret
		}
	finally:
		util.close(conn)

def __main():
	obj = req_json('GET', 'https://api.github.com/users/murer/keys', headers = {
		'User-Agent': 'dsopz'
	}, expects = [200])
	print(obj)

if __name__ == '__main__':
	__main()
