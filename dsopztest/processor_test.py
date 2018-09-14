import unittest
import time
from dsopz.processor import Processor
from concurrent.futures import ThreadPoolExecutor

class Task(object):

    def __init__(self):
        self.total = 0

    def task(self, a):
        time.sleep(1)
        print('sum', a)
        self.total = self.total + a

class TestCase(unittest.TestCase):

    def test_job(self):
        task = Task()
        with Processor(1) as p:
            p.submit(task.task, 1)
            p.submit(task.task, 2)
            p.submit(task.task, 4)
            p.submit(task.task, 8)
        self.assertEqual(15, task.total)

if __name__ == '__main__':
    unittest.main()
