import unittest
from dsopztest import abstract_test_case
from dsopz.query import run_query

class TestCase(abstract_test_case.TestCase):

    def test_run_query(self):
        result = run_query(
            'dsopzproj',
            '',
            'select * from notfound',
            0,
            10,
            'startcursor',
            'endcursor'
        )
        print(result)
        self.assertEqual(1, len(result))

if __name__ == '__main__':
    unittest.main()
