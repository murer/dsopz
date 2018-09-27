from dsopz import util
import gzip
import json as JSON

class Error(Exception):
    """Exceptions"""

class Writer(object):

    def __init__(self, f, gz=False):
        if not f:
            raise Error('not f')
        if f == '-':
            f = sys.stdout
        should_close = False
        if isinstance(f, str):
            should_close = True
            f = open(f, 'wb')
        self._plain_file = f
        if gz:
            f = gzip.open(f, 'wb')
        self._wrapper = f
        self._should_close = should_close

    def write(self, line):
        data = '%s\n' % (line)
        data = data.encode('UTF-8')
        self._wrapper.write(data)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        if self._should_close:
            util.close(self._wrapper)
            util.close(self._plain_file)

class Reader(object):

    def __init__(self, f, gz=False):
        if not f:
            raise Error('not f')
        if f == '-':
            f = sys.stdin
        should_close = False
        if isinstance(f, str):
            should_close = True
            f = open(f, 'rb')
        self._plain_file = f
        if gz:
            f = gzip.open(f, 'rb')
        self._wrapper = f
        self._should_close = should_close

    def __next__(self):
        ret = next(self._wrapper)
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
        if self._should_close:
            util.close(self._wrapper)
            util.close(self._plain_file)

class JWriter(Writer):

    def write(self, line):
        data = JSON.dumps(line)
        return super().write(data)

class JReader(Reader):

    def __next__(self):
        data = super().__next__()
        return JSON.loads(data)
