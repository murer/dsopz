from concurrent.futures import ThreadPoolExecutor

def task():
    print('task')

class Processor(object):

    def __init__(self, max_workers):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.pool.submit(task)

    def shutdown(self):
        self.pool.shutdown(wait=True)
        print('shutdown')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.shutdown()

    def submit(self, fn, *args, **kwargs):
        return self.pool.submit(fn, *args, **kwargs)
