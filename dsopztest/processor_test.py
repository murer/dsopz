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
        return self.total

class TestCase(unittest.TestCase):

    def test_job(self):
        task = Task()
        with Processor(10) as p:
            print(p.submit(task.task, 1).result())
            print(p.submit(task.task, 2).result())
            print(p.submit(task.task, 4).result())
            print(p.submit(task.task, 8).result())
        self.assertEqual(15, task.total)

if __name__ == '__main__':
    unittest.main()
