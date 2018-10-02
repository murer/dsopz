import unittest
from dsopztest import abstract_test_case
from dsopz import http
import json as JSON
from dsopz.processor import dispatch

class HttpTest(abstract_test_case.TestCase):

    def test_sync(self):
        self.assertEqual(404, http.req_text('POST', 'http://localhost:8082/not-found', expects=[404])['status'])

        self.assertEqual(404, dispatch(
            http.req_text, 'POST', 'http://localhost:8082/not-found', expects=[404]
        ).result()['status'])

        self.assertIsInstance(dispatch(
            http.req_text, 'POST', 'http://localhost:8082/not-found'
        ).exception(), http.Error)



if __name__ == '__main__':
    unittest.main()
