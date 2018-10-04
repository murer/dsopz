import threading
#from concurrent.futures import Future
from queue import Queue

class Error(Exception):
    """Exceptions"""

class Future(object):

    def __init__(self):
        self._result = None
        self._status = 0
        self._lock = threading.Condition()

    def set_running_or_notify_cancel(self):
        with self._lock:
            self._status = 1
            return False

    def set_result(self, result):
        with self._lock:
            if self._status != 1:
                raise Error('illegal state: %s' % (self._status))
            print('set_result')
            self._result = (None, result)
            self._status = 2
            self._lock.notify_all()
            print('set_resulted')

    def set_exception(self, exception):
        with self._lock:
            if self._status != 1:
                raise Error('illegal state: %s' % (self._status))
            print('set_exception')
            self._result = (exception, None)
            self._status = 2
            self._lock.notify_all()
            print('set_exceptioned')

    def done(self):
        with self._lock:
            return self._status != 1

    def resolve(self):
        with self._lock:
            if self._status == 0:
                raise Error('illegal state: %s' % (self._status))
            if self._status == 2:
                return self._result
            print('resolve')
            self._lock.wait()
            print('resolved')
            self._status = 2
            return self._result

    def result(self):
        print('fjsdklfhdsk')
        ret = self.resolve()
        print('result', ret)
        if ret[0]:
            raise ret[0]
        return ret[1]

    def exception(self):
        ret = self.resolve()
        print('exception', ret)
        return ret[0]

def _work(future, fn, args, kwargs):
    future.set_running_or_notify_cancel()
    try:
        ret = fn(*args, **kwargs)
    except BaseException as exc:
        future.set_exception(exc)
    else:
        future.set_result(ret)

def dispatch(fn, *args, **kwargs):
    ret = Future()
    thread = threading.Thread(target=_work, args=[ret, fn, args, kwargs])
    thread.start()
    return ret

def blockify(array, block_size, filter=None, skip=0):
    ret = []
    count = 0
    for i in array:
        if filter:
            i = filter(i)
        if i != None:
            count = count + 1
            if count > skip:
                ret.append(i)
                if len(ret) >= block_size:
                    yield ret
                    ret = []
    if skip > count:
        raise Error('skip %s > count %s' % (skip, count))
    if len(ret) > 0:
        yield ret

def merge_gens(arrays):
    while True:
        stop = True
        for idx, array in enumerate(arrays):
            try:
                yield (idx, next(array))
                stop = False
            except StopIteration:
                pass
        if stop:
            return

def _async_gen_work(gen, q):
    for i in gen:
        q.put((False, i))
    q.put((True, None))

def async_gen(gen, maxsize=10):
    q = Queue(maxsize=maxsize)
    fut = dispatch(_async_gen_work, gen, q)
    while True:
        done, ret = q.get()
        if done:
            fut.result()
            return
        yield ret
