import os
import unittest
import json

from v1.apps import app, db, socketio
from v1.apps.users.models import User
from v1.apps.safehouse.guests.models import Guest
from v1.apps.safehouse.hosts.models import Host, Suspend
from v1.apps.safehouse.models import Trait

from v1.apps.config import DATABASE_TEST

from flask_socketio import SocketIO, SocketIOTestClient

from datetime import date

class TestingBase(unittest.TestCase):
    def initDB(self):
        for i in range(20):
            user = User(username="TestUser" + str(i))
            user.hash_password("password")
            if i == 0:
                user.admin = True
            if i <= 10: #Create Guest
                guest = Guest(user=user, traits=Trait(), requirements=Trait())
            else:
                host = Host(user=user, traits=Trait(), requirements=Trait())
            self.db.session.add(user)
        self.db.session.commit()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_TEST
        self.app = app.test_client()
        self.db = db
        self.db.create_all()
        self.socketio = SocketIOTestClient(app, socketio)
        self.initDB()


    def tearDown(self):
        self.socketio.disconnect()
        self.db.session.expunge_all()
        self.db.session.flush()
        self.db.session.remove()
        self.db.session.close()
        self.db.drop_all()


class SafeHouseTesting(TestingBase):
    base_url = '/api/v1'

    def login(self, username, password):
        payload = {'username':username, 'password': password}
        url = self.base_url + '/users/login'
        return self.app.post(url, data=json.dumps(payload), content_type='application/json', follow_redirects=True)

    def register(self, username, password):
        payload = {'username':username, 'password': password}
        url = self.base_url + '/users/register'
        return self.app.post(self.base_url + '/register', data=json.dumps(payload), content_type='application/json', follow_redirects=True)
