import json
import unittest
from base64 import b64encode
from unittest import skip

from werkzeug.datastructures import MultiDict

import pre_flight
import database_manager
from pre_flight import app
from unittest import mock, skip
from mock import patch
import mongomock 


class PreFlightTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        pre_flight.template_to_use = 'test_template.xml'

    def tearDown(self):
        pre_flight.template_to_use = 'template.xml'

    def test_get_new_mission(self):
        headers = {
            'Authorization': 'Basic ' + b64encode(bytes("Test:Test", 'ascii')).decode('ascii')
        }
        response = self.app.get('/new-mission', follow_redirects=True, headers=headers)
        expected_result = b'<h1>New flight mission</h1>\n\n<p><form name="overall" id="root-form"><div>Pilot name<input type="text" id="text-Pilot-name" name="Pilot-name" value="" /></div><br /><div>Co-Pilot name<input type="text" id="text-Co-Pilot-name" name="Co-Pilot-name" value="" /></div><br /><div>Flight height<input type="text" id="text-Flight-height" name="Flight-height" value="100" /></div><br />Flight mode<div id="Flight-mode"><input type="radio" id="Flight-modeOpen" name="Flight-mode" onchange="changeVisibilityRadio(\'Open\', \'Flight-modeOpen\', \'Flight-mode\')"/><label for="Flight-modeOpen">Open</label><input type="radio" id="Flight-modeSpecified" name="Flight-mode" onchange="changeVisibilityRadio(\'Specified\', \'Flight-modeSpecified\', \'Flight-mode\')"/><label for="Flight-modeSpecified">Specified</label><input type="radio" id="Flight-modeCertified" name="Flight-mode" onchange="changeVisibilityRadio(\'Certified\', \'Flight-modeCertified\', \'Flight-mode\')"/><label for="Flight-modeCertified">Certified</label><div id="Open" class="Flight-mode" style="display:none"></div><div id="Specified" class="Flight-mode" style="display:none"><div id="SORA-needed-div"><label for="SORA-needed">SORA needed</label><input type="checkbox" id="SORA-needed" name="SORA-needed" onchange="changeVisibilityCheckbox(\'SORA-needed-children-div\', \'SORA-needed\')"/><div id="SORA-needed-children-div" style="display:none"><div>SORA<input type="file" id="upload-file-SORA" name="SORA" /></div><br /></div></div><br /><div id="Police-approval-needed-div"><label for="Police-approval-needed">Police approval needed</label><input type="checkbox" id="Police-approval-needed" name="Police-approval-needed" onchange="changeVisibilityCheckbox(\'Police-approval-needed-children-div\', \'Police-approval-needed\')"/><div id="Police-approval-needed-children-div" style="display:none"><div>Police approval<input type="file" id="upload-file-Police-approval" name="Police-approval" /></div><br /></div></div><br /><div id="Land-owner-permit-needed-div"><label for="Land-owner-permit-needed">Land owner permit needed</label><input type="checkbox" id="Land-owner-permit-needed" name="Land-owner-permit-needed" onchange="changeVisibilityCheckbox(\'Land-owner-permit-needed-children-div\', \'Land-owner-permit-needed\')"/><div id="Land-owner-permit-needed-children-div" style="display:none"><div>Land owner permit<input type="file" id="upload-file-Land-owner-permit" name="Land-owner-permit" /></div><br /></div></div><br /></div><div id="Certified" class="Flight-mode" style="display:none"></div></div><br /><div>Comment<br/><textarea rows="10" cols="100" class="comment" id="multiline-Comment" name="multiline" placeholder="Write comment here if you are ugly as f*ck lmao..."></textarea></div><br /><input type="button" value="Create mission" onclick="validateSubmit(&quot;root-form&quot;)" /></form></p>\n<div id="errorMessage" style="display:none">You have to fill out all the forms!</div>\n<div id="serverErrorMessage" style="display:none">Something went wrong, try again!</div>\n<div id="successMessage" style="display:none">The mission have been uploaded!</div>'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_result, response.data)

    def test_get_new_mission_unauthorized(self):
        response = self.app.get('/new-mission', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_save_mission(self):
        client = mongomock.MongoClient()
        with mock.patch(database_manager.__connect_to_db, return_value=client):
            yield client

        data_to_send = MultiDict([('Pilot-name', 'test'), ('Co-Pilot-name', 'test'), ('Flight-height', '100'), ('Flight-mode', 'Open'), ('Comment', 'test comment')])
        response = self.app.post('/save-mission', data=data_to_send, follow_redirects=True)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['result'][0])

    def test_save_mission_when_none(self):
        client = mongomock.MongoClient()
        with mock.patch(database_manager.__connect_to_db, return_value=client):
            yield client

        data_to_send = None
        response = self.app.post('/save-mission', data=data_to_send, follow_redirects=True)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'][0], True)

    def test_save_mission_when_data_is_wrong(self):
        client = mongomock.MongoClient()
        with mock.patch(database_manager.__connect_to_db, return_value=client):
            yield client
        
        data_to_send = MultiDict([('Flight-test','0'),('Flight-something','not-open'),('Comment', '')])
        response = self.app.post('/save-mission', data=data_to_send, follow_redirects=True)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'][0], True)

