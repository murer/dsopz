import unittest
import time
from dsopz.processor import Processor
from concurrent.futures import Future

class Error(Exception):
	"""Exceptions"""

class Task(object):

    def __init__(self):
        self.total = 0

    def task(self, a):
        if a == 'error':
            raise Error()
        time.sleep(0.0002)
        self.total = self.total + a
        return self.total

class ProcessorTest(unittest.TestCase):

    def test_job(self):
        task = Task()
        with Processor('p', 10) as p:
            self.assertTrue(isinstance(p.submit(task.task, 1), Future))
            self.assertTrue(isinstance(p.submit(task.task, 2), Future))
            self.assertTrue(isinstance(p.submit(task.task, 4), Future))
            self.assertTrue(isinstance(p.submit(task.task, 8), Future))
        self.assertEqual(15, task.total)

    def test_future(self):
        task = Task()
        with Processor('p', 10) as p:
            self.assertEqual(1, p.submit(task.task, 1).result(2))
            self.assertEqual(3, p.submit(task.task, 2).result(2))
        self.assertEqual(3, task.total)

    def test_exp(self):
        task = Task()
        with Processor('p', 10) as p:
            self.assertEqual(Error, p.submit(task.task, 'error').exception(2).__class__)

    def test_large(self):
        task = Task()
        with Processor('p', 10) as p:
            for k in range(1000):
                p.submit(task.task, 1)
        self.assertEqual(1000, task.total)



if __name__ == '__main__':
    unittest.main()
