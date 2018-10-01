import threading
from concurrent.futures import Future

def _work(future, fn, args, kwargs):
    future.set_running_or_notify_cancel()
    ret = fn(*args, **kwargs)
    future.set_result(ret)

def async(fn, *args, **kwargs):
    ret = Future()
    thread = threading.Thread(target=_work, args=[ret, fn, args, kwargs])
    thread.start()
    return ret
