import os, errno

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
