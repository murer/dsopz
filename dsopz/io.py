
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
