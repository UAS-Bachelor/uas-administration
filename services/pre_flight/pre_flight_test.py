import unittest

from pre_flight import app


class PreFlightTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_main_page(self):
        response = self.app.get('/new-mission', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

