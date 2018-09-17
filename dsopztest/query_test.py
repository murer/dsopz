from dsopztest import abstract_test_case
from dsopz.query import Query

class TestCase(abstract_test_case.TestCase):

    def test_query(self):
        result = Query(
            'dataset',
            'namespace',
            'select *',
            0,
            10,
            'startcursor',
            'endcursor'
        ).execute()
        self.assertEqual(1, len(result))

if __name__ == '__main__':
    unittest.main()
