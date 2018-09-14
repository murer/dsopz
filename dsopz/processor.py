from concurrent.futures import ThreadPoolExecutor

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
