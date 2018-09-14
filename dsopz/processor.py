
class Processor(object):

    def __init__(self, max):
        self.max = max

    def start(self):
        print('start')
        return self

    def shutdown(self):
        print('shutdown')

    def __enter__(self):
        return self.start()

    def __exit__(self, exception_type, exception_value, traceback):
        self.shutdown()

    def submit(self, name, priority, fn):
        print('submit', fn)
