import threading
from concurrent.futures import Future

def _work(future, fn, args, kwargs):
    future.set_running_or_notify_cancel()
    try:
        ret = fn(*args, **kwargs)
    except BaseException as exc:
        future.set_exception(exc)
    else:
        future.set_result(result)
    
def async(fn, *args, **kwargs):
    ret = Future()
    thread = threading.Thread(target=_work, args=[ret, fn, args, kwargs])
    thread.start()
    return ret
