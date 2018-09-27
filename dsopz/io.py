from dsopz import util
import gzip
import json as JSON
import sys

class Error(Exception):
    """Exceptions"""

class Writer(object):

    def __init__(self, f, gz=False, append=False):
        self._closable_plain = None
        self._closable_gz = None
        if not f:
            raise Error('not f')
        if f == '-':
            self._writer = sys.stdout.buffer
        elif isinstance(f, str):
            self._writer = open(f, 'ab' if append else 'wb')
            self._closable_plain = self._writer
        if gz:
            self._writer = gzip.open(self._writer, 'wb')
            self._closable_gz = self._writer

    def write(self, line):
        data = '%s\n' % (line)
        data = data.encode('UTF-8')
        self._writer.write(data)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        util.close(self._closable_gz)
        util.close(self._closable_plain)

class Reader(object):

    def __init__(self, f, gz=False):
        self._closable_plain = None
        self._closable_gz = None
        if not f:
            raise Error('not f')
        if f == '-':
            self._reader = sys.stdin.buffer
        elif isinstance(f, str):
            self._reader = open(f, 'rb')
            self._closable_plain = self._reader
        if gz:
            self._reader = gzip.open(self._reader, 'rb')
            self._closable_gz = self._reader

    def __next__(self):
        ret = next(self._reader)
        ret = ret.decode('UTF-8')
        ret = ret.strip()
        return ret

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        util.close(self._closable_gz)
        util.close(self._closable_plain)

class JWriter(Writer):

    def write(self, line):
        data = JSON.dumps(line)
        return super().write(data)

class JReader(Reader):

    def __next__(self):
        data = super().__next__()
        return JSON.loads(data)

def jreader(plain = None, gz = None):
    if not plain and not gz:
        raise Error('not plain and not gz')
    if plain and gz:
        raise Error('plain and gz')
    if gz:
        plain = gz
        gz = True
    else:
        gz = False
    return JReader(plain, gz)

def jwriter(plain = None, gz = None, append=False):
    if not plain and not gz:
        raise Error('not plain and not gz')
    if plain and gz:
        raise Error('plain and gz')
    if gz:
        plain = gz
        gz = True
    else:
        gz = False
    return JWriter(plain, gz=gz, append=append)
