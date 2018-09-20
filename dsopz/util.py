import os
import errno
import json
import socket
import time
import socket

class Error(Exception):
	"""Exceptions"""

def close(obj):
    try:
        obj.close()
    except:
        """ Done """

def makedirs(directory):
    os.makedirs(str(directory), exist_ok=True)

def check_port(host, port):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        close(sock)

def wait_check_port(host, port, sleep=0.1, times=20):
    for i in range(times):
        if check_port(host, port):
            return
        time.sleep(sleep)
    raise Error('timeout %s:%s', host, port)
