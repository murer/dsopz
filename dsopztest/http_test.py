import unittest
from dsopztest import abstract_test_case
from dsopz import http
import json as JSON
from dsopz.async import async

class HttpTest(abstract_test_case.TestCase):

    def test_sync(self):
        self.assertEqual(404, http.req_text('POST', 'http://localhost:8082/not-found', expects=[404])['status'])

    def test_async(self):
        fut = async(http.req_text, 'POST', 'http://localhost:8082/not-found', expects=[404])
        resp = fut.result()
        self.assertEqual(404, resp['status'])

if __name__ == '__main__':
    unittest.main()
