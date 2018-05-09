import unittest

import database_manager


class PreFlightDatabaseTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_mission(self):
        test_mission = { 'pilot': 'TestPilot'}
        #result, msg = database_manager.create_mission(test_mission)
        #self.assertTrue(result, msg)

