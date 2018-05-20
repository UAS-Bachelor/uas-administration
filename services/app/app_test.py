import unittest

from flask_login import current_user

import database_manager
from app import app


class AppTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        database_manager.database = "uas-administration-dev"

    def test_get_new_mission_without_login(self):
        response = self.app.get('/new-mission')
        # should be 302, because it will redirect to the login page, if not logged in
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        with self.app:
            self.app.post('/login', data={'username': 'Test', 'password': 'Test'})
            self.assertTrue(current_user.username == 'Test')

    def test_logout(self):
        with self.app:
            self.app.post('/login', data={'username': 'Test', 'password': 'Test'})
            self.assertTrue(current_user.username == 'Test')
            self.assertFalse(current_user.is_anonymous)
            self.app.get('/logout')
            self.assertTrue(current_user.is_anonymous)

    def test_get_new_mission_with_login(self):
        with self.app:
            self.app.post('/login', data={'username': 'Test', 'password': 'Test'})
            response = self.app.get('/new-mission')
            self.assertEqual(response.status_code, 200)
