from io import BufferedIOBase, TextIOBase
from dsopz import util

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


class Stream(BufferedIOBase):

    def __init__(self, f, mode, gzip=False):
        if not mode:
            raise Error('mode is required')
        if 'b' in mode:
            raise Error("'b' in mode")
        if not mode.startswith('w') and not mode.startswith('r'):
            raise Error("not mode.startswith('w') and not mode.startswith('r')")
        if not f:
            raise Error('not f')
        if f == '-':
            f = sys.stdout if mode.startswith('w') else sys.stdin
        should_close = False
        if isinstance(f, str):
            nmode = mode + 'b'
            print('mode', nmode)
            f = open(f, nmode)
            should_close = True
        if gzip:
            f = gzip(f) if mode.startswith('w') else gunzip(f)
        f = TextIOBase(f)
        self._wrapper = f
        self._should_close = should_close

    def read(self, size=-1):
        ret = self._wrapper.read(size)
        print('ret', type(ret), ret)
        return ret

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        if self._should_close:
            util.close(self._wrapper)
