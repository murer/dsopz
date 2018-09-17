from dsopztest import abstract_test_case
from dsopz.query import runQuery

class TestCase(abstract_test_case.TestCase):

    def test_query(self):
        result = runQuery(
            'dataset',
            'namespace',
            'select * from notfound',
            0,
            10,
            'startcursor',
            'endcursor'
        )
        self.assertEqual(1, len(result))

if __name__ == '__main__':
    unittest.main()
