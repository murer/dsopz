from concurrent.futures import Executor, Future
import threading

"""
class Processor(object):

    def __init__(self, name, max_workers):
        self.name = name
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def shutdown(self):
        self.pool.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.shutdown()

    def submit(self, fn, *args, **kwargs):
        return self.pool.submit(fn, *args, **kwargs)
"""

class Processor(Executor):

    def __init__(self, name, max_workers):
        self.name = name

    def shutdown(self):
        """ implement """

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.shutdown()

    def _work(self, future, fn, args, kwargs):
        if not future.set_running_or_notify_cancel():
            return
        result = fn(*args, *kwargs)
        future.set_result(result)

    def submit(self, fn, *args, **kwargs):
        ret = Future()
        thread = threading.Thread(target=self._work, args=[ret, fn, args, kwargs])
        thread.start()
        return ret
