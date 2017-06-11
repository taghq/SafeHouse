from v1.apps import db

import datetime

class Host(db.Model):
    __tablename__ = 'host'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    preference = db.relationship("Preference", uselist=False, backref="host")

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

class Preference(db.Model):
    __tablename__ = 'preference'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(32))
    wheelchair_access=db.Column(db.Boolean, default=False)
    smoking_allowed=db.Column(db.Boolean, default=False)
    pets_allowed=db.Column(db.Boolean, default=False)
    has_pets=db.Column(db.Boolean, default=False)
    overnight_stays_allowed=db.Column(db.Boolean, default=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))

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
