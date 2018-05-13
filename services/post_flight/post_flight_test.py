import unittest
from base64 import b64encode

import database_manager
from post_flight import app


class PostFlightTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        database_manager.database = "uas-administration-dev"

    def test_view_missions(self):
        headers = {
            'Authorization': 'Basic ' + b64encode(bytes("Test:Test", 'ascii')).decode('ascii')
        }
        response = self.app.get('/view-missions', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_view_missions_unauthorized(self):
        response = self.app.get('/view-missions')
        self.assertEqual(response.status_code, 401)

    def test_view_mission(self):
        headers = {
            'Authorization': 'Basic ' + b64encode(bytes("Test:Test", 'ascii')).decode('ascii')
        }
        response = self.app.get('/view-mission/5af85ee3d88c2a3e88615a5c', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_view_nonexisting_mission(self):
        headers = {
            'Authorization': 'Basic ' + b64encode(bytes("Test:Test", 'ascii')).decode('ascii')
        }
        response = self.app.get('/view-mission/1', headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_view_mission_unauthorized(self):
        response = self.app.get('/view-mission/5af85ee3d88c2a3e88615a5c')
        self.assertEqual(response.status_code, 401)


