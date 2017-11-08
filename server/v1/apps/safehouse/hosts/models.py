from v1.apps import db
from v1.apps.safehouse.models import Trait

import datetime

class Host(db.Model):
    __tablename__ = 'host'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    traits = db.relationship("Trait", uselist=False, backref="host_traits")
    requirements = db.relationship("Trait", uselist=False, backref="host_requirements")

    def is_available(self, date):
        if type(date) is not datetime.date:
            raise TypeError('arg must be a datetime.date, not a %s' % type(date))
        for suspended_date in self.suspended_dates:
            if date >= suspended_date.from_date and date <= suspended_date.to_date:
                return False
        return True

class Location(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String(64))
    address2 = db.Column(db.String(64))
    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    host = db.relationship('Host', backref=db.backref('location', lazy='dynamic'))

class Suspend(db.Model):
    __tablename__ = 'suspend'
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    host = db.relationship('Host', backref=db.backref('suspended_dates', lazy='dynamic'))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)

    def is_available(self, date):
        if type(date) is not datetime.date:
            raise TypeError('arg must be a datetime.date, not a %s' % type(date))
        if date >= self.from_date and date <= self.to_date:
            return False
        else:
            return True
