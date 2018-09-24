import unittest

class SampleTest(unittest.TestCase):

    def test1(self):
        self.assertEqual(1, 1)

    def testB(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
