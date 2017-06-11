import os
import unittest
import json

from v1.apps import app, db, socketio
from v1.apps.users.models import User
from v1.apps.safehouse.guests.models import Guest, Trait
from v1.apps.safehouse.hosts.models import Host, Preference, Suspend

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
                guest = Guest(user=user)
                trait = Trait(guest=guest, language="English", disabled=True, smoker=True, has_pets=False)
            else:
                host = Host(user=user)
                preference = Preference(host=host, language="Spanish")
                suspend = Suspend(from_date=date(2017,6,1), to_date=date(2017,6,14))
                host.suspended_dates.append(suspend)
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

    def doStuff():
        return True
