import unittest
from dsopz.processor import Processor
from concurrent.futures import ThreadPoolExecutor

def task(a, b):
    ret = a + b
    print('task', ret)
    return ret

class TestCase(unittest.TestCase):

    def test_job(self):
        with Processor(1) as p:
            p.submit(task, 3, 4)
            p.submit(task, 3, 4)
            p.submit(task, 3, 4)
            p.submit(task, 3, 4)

if __name__ == '__main__':
    unittest.main()
