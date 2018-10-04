import threading
from concurrent.futures import Future

class Error(Exception):
    """Exceptions"""

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

def _work_with_future(future, fn, args, kwargs):
    future.set_running_or_notify_cancel()
    try:
        ret = fn(future, *args, **kwargs)
    except BaseException as exc:
        future.set_exception(exc)
    else:
        future.set_result(ret)

def dispatch_with_future(fn, *args, **kwargs):
    ret = Future()
    thread = threading.Thread(target=_work_with_future, args=[ret, fn, args, kwargs])
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
        print('put', i)
        q.put((False, i))
    q.put((True, None))

def async_gen(gen, maxsize=10):
    from queue import Queue
    q = Queue(maxsize=maxsize)
    fut = dispatch_with_future(_async_gen_work, gen, q)
    while True:
        done, ret = q.get()
        print('get', done, ret, fut.done())
        fut.cancel()
        if done:
            return
        yield ret

    """
    elements = []
    try:
        while True:
            while len(elements) < maxsize:
                elements.append(dispatch(lambda x: next(x), gen))
            element = elements.pop(0)
            yield element.result()
    except StopIteration:
        pass
    finally:
        while len(elements) > 0:
            elements.pop(0).exception()
    """
