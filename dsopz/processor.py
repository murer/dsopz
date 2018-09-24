from concurrent.futures import Executor, Future
from queue import Queue
import threading

class Error(Exception):
	"""Exceptions"""

class Processor(Executor):

    def __init__(self, name, max_workers):
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._name = name
        self._queue = Queue(maxsize=max_workers*10)
        self._threads = []
        for i in range(max_workers):
            thread = threading.Thread(target=self._work)
            self._threads.append(thread)
            thread.start()

    def shutdown(self):
        with self._shutdown_lock:
            self._shutdown = True
            for _ in self._threads:
                self._queue.put([None, None, None, None])
        self._queue.join()
        for thread in self._threads:
            thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.shutdown()

    def _work(self):
        while True:
            future, fn, args, kwargs = self._queue.get()
            if not future:
                self._queue.task_done()
                return
            if not future.set_running_or_notify_cancel():
                return
            try:
                result = fn(*args, *kwargs)
            except BaseException as exc:
                future.set_exception(exc)
            else:
                future.set_result(result)
            finally:
                self._queue.task_done()
        return True

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise Error('cannot schedule new futures after shutdown')
            ret = Future()
            self._queue.put([ret, fn, args, kwargs])
            return ret
