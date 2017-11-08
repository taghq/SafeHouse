from . import SafeHouseTesting
from v1.apps.users.models import User

import requests, json

class RequestsTests(SafeHouseTesting):

    def login(self):
        username = "TestUser1"
        rv = self.login(username, "password")
        data = json.loads(rv.data.decode('utf-8'))
        assert username in data['username']

    def register_user(self):
        username = "NewUser"
        rv = self.register(username, "password")
        data = json.loads(rv.data.decode('utf-8'))
        assert username in data['username']

    def register_guest_host(self):
        username = "TestUser12"
        password = "password"
        payload = {
            'username':username,
            'password': password,
            }
        #Test registering guest
        url = self.base_url + '/safehouse/guests/register'
        rv = self.app.post(url, data=json.dumps(payload), content_type='application/json', follow_redirects=True)
        data = json.loads(rv.data.decode('utf-8'))
        print(data)
        # Test Registering host
        username = "TestUser1"
        password = "password"
        payload = {
            'username':username,
            'password': password,
            }
        url = self.base_url + '/safehouse/hosts/register'
        rv = self.app.post(url, data=json.dumps(payload), content_type='application/json', follow_redirects=True)
        data = json.loads(rv.data.decode('utf-8'))
        print(data)

    def test_set_traits(self):
        username = "TestUser1"
        password = "password"
        payload = {
            'username':username,
            'password': password,
            'language': "spanish",
            'smoker': True,
            'FAKEDATA': None,
            }
        url = self.base_url + '/safehouse/guests/traits'
        rv = self.app.post(url, data=json.dumps(payload), content_type='application/json', follow_redirects=True)
        data = json.loads(rv.data.decode('utf-8'))
        print(data)
