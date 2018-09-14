import unittest
from dsopz.processor import Processor

def task():
    return None

class TestCase(unittest.TestCase):

    def test_job(self):
        with Processor(max=1) as p:
            p.submit('n1', 0, task)

if __name__ == '__main__':
    unittest.main()
