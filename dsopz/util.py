from __future__ import print_function
import os
import errno
import json
import sys


def prn(dest, *args):
	print(*args, file=dest)

def close(obj):
	try:
		obj.close()
	except:
		""" Done """

def makedirs(directory):
	try:
		os.makedirs(directory)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(directory):
			pass
		else:
			raise
