from app import app

import unittest

class UnitTest(unittest.TestCase):

  def test_should_have_ping_endpoint(self):
    test_app = app.test_client(self)
    response = test_app.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, b"PING")

if __name__ == '__main__':
    unittest.main()
