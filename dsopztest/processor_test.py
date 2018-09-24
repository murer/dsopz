import unittest
import time
from dsopz.processor import Processor
from concurrent.futures import Future

class Task(object):

    def __init__(self):
        self.total = 0

    def task(self, a):
        time.sleep(0.1)
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
            a = p.submit(task.task, 1)
            b = p.submit(task.task, 2)
            self.assertEqual(1, a.result(2))
            self.assertEqual(3, b.result(2))
        self.assertEqual(3, task.total)

if __name__ == '__main__':
    unittest.main()
