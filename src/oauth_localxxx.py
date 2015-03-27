from oauth2client import client
import util
import os
import webbrowser
from oauth2client import tools
try:
  # pylint:disable=g-import-not-at-top
  from urlparse import parse_qsl
except ImportError:
  # pylint:disable=g-import-not-at-top
  from cgi import parse_qsl

class Error(Exception):
	"""Exceptions for the flow module."""

class AuthRequestRejectedException(Error):
	"""Exception for when the authentication request was rejected."""

class Token():
	token = None

class ClientRedirectHandler(tools.ClientRedirectHandler):
	def do_GET(self):
		query = self.path.split('?', 1)[-1]
		query = dict(parse_qsl(query))
		self.server.query_params = query
		if 'code' in query:
			msg = 'Done'
		else:
			msg = 'Access Denied'
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(msg)

def __retrieve_local():
	httpd = tools.ClientRedirectServer(('localhost', 7005), ClientRedirectHandler)
	flow = client.flow_from_clientsecrets('conf/client.json.secret',
    								  	  scope='https://www.googleapis.com/auth/taskqueue.consumer',
	   									  redirect_uri='http://localhost:7005/redirect_uri')
	auth_uri = flow.step1_get_authorize_url()
	webbrowser.open(auth_uri, new=1, autoraise=True)
	httpd.handle_request()
	if 'error' in httpd.query_params:
		raise AuthRequestRejectedException('Unable to authenticate.')
	code = httpd.query_params['code']
	credential = flow.step2_exchange(code)
	return credential.access_token

def __retrieve_file():
	f = None
	try:
		f = open('tmp/cloudz_local_token.tmp', 'r')
		return f.readline()
	except IOError:
		return None
	finally:
		util.close(f)

def __write_file():
	f = None
	try:
		os.makedirs('tmp')
		f = open('tmp/cloudz_local_token.tmp', 'w')
		f.truncate()
		f.write(Token.token)
	finally:
		util.close(f)

def get_token():
	if(Token.token == None):
		Token.token = __retrieve_file()
	if(Token.token == None):
		Token.token = __retrieve_local()
		__write_file()
	return Token.token

def main():
	token = get_token();
	print 'access_token: ' + token
	token = get_token();
	print 'access_token: ' + token

if __name__ == '__main__':
	main()
