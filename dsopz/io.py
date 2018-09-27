from io import BufferedIOBase, TextIOBase
from dsopz import util
import gzip

class Error(Exception):
    """Exceptions"""

def stream(f=None, fgz=None, mode=None):
    if not mode:
        raise Error('mode is required')
    if not mode.startswith('w') and not mode.startswith('r'):
        raise Error("not mode.startswith('w') and not mode.startswith('r')")
    if not f and not fgz:
        raise Error('not f and not fgz')
    if f and fgz:
        raise Error('f and fgz')
    f = f or fgz
    if f == '-' and not std:
        raise Error("f == '-' and not std")
    if f == '-':
        f = sys.stdout if mode.startswith('w') else sys.stdin
    should_close = False
    if isinstance(f, str):
        f = open(f, mode)
        should_close = True
    if fgz:
        f = gzip(f) if mode.startswith('w') else gunzip(f)
    return (f, should_close)

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
