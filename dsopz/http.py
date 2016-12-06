import httplib
import json
import util
import threading
from urlparse import urlparse

class Error(Exception):
	"""Exceptions"""

class HttpError(Error):
	"""Exception"""

def req_json(method, url, params = '', headers = {}, expects = [200]):
	parsed = urlparse(url)
	host = parsed.netloc
	uri = parsed.path
	if(parsed.query != ''):
		uri = uri + '?' + parsed.query
	conn = None
	if(parsed.scheme == 'https'):
		conn = httplib.HTTPSConnection(parsed.hostname, parsed.port or 443)
	else:
		conn = httplib.HTTPConnection(parsed.hostname, parsed.port or 80)
	if parsed.username != None:
		token = parsed.username + ':' + (parsed.password or '')
		token = 'Basic ' + base64.b64encode(token)
		headers['Authorization'] = token
	success = False
	try:
		conn.request(method, uri, params, headers)
		response = conn.getresponse()
		if response.status not in expects:
			raise Error('Status: %d %s %sri' % (response.status, response.reason, response.read()))
		string = response.read()
		if not string:
			return None
		ret = json.loads(string)
		success = True
		return ret
	finally:
		util.close(conn)

class HttpThread(threading.Thread):

	def __init__(self, method, url, params, headers, expects):
		threading.Thread.__init__(self)
		self.method = method
		self.url = url
		self.params = params
		self.headers = headers
		self.expects = expects
		self.response = None
		self.status = 'CREATED'

	def run(self):
		try:
			self.status = 'REQUESTING'
			self.response = req_json(self.method, self.url, self.params, self.headers, self.expects)
			self.status = 'DONE'
		finally:
			if self.status != 'DONE':
				self.status = 'ERROR'

	def resp(self):
		while self.status != 'DONE' and self.status != 'ERROR':
			self.join()
		if self.status == 'DONE':
			return self.response
		raise Error('Error on http thread, status: %s' % (self.status))

def async_req_json(method, url, params = '', headers = {}, expects = [200]):
	thread = HttpThread(method, url, params, headers, expects)
	thread.start()
	return thread

def __main():
	obj = async_req_json('GET', 'https://api.github.com/users/murer', headers = {
		'User-Agent': 'dsopz'
	}, expects = [200]).resp()
	print json.dumps(obj, indent=True)

if __name__ == '__main__':
	__main()
