import oauth_installed
import sys
import http
import json

def get_token():
	return oauth_installed.get_token()

def oauth_req_json(method, url, params = None, headers = {}, expects = [200]):
	return oauth_async_req_json(method, url, params, headers, expects).resp()

def oauth_async_req_json(method, url, params = None, headers = {}, expects = [200]):
	headers['Authorization'] = 'Bearer %s' % get_token()
	if params:
		params = json.dumps(params)
		headers['Content-type'] = 'application/json; charset=UTF-8'	
	return http.async_req_json(method, url, params, headers, expects)

def __main():
	print get_token()

if __name__ == '__main__':
	__main()

