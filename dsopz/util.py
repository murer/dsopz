import os
import errno
import json

def close(obj):
	try:
		obj.close()
	except:
		""" Done """

def makedirs(directory):
	os.makedirs(str(directory), exist_ok=True)
