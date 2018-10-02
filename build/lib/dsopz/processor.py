import threading
from concurrent.futures import Future

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

def blockify(array, block_size, filter=None):
    ret = []
    for i in array:
        if filter:
            i = filter(i)
        if i != None:
            ret.append(i)
            if len(ret) >= block_size:
                yield ret
                ret = []
    if len(ret) > 0:
        yield ret
