from v1.apps import db

class Trait(db.Model):
    __tablename__ = 'trait'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(32))
    disabled=db.Column(db.Boolean, default=False)
    smoker=db.Column(db.Boolean, default=False)
    pets_allowed=db.Column(db.Boolean, default=False)
    has_pets=db.Column(db.Boolean, default=False)
    overnight_stay=db.Column(db.Boolean, default=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
