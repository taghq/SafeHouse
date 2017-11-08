from v1.apps import db
from v1.apps.safehouse.models import Trait

class Guest(db.Model):
    __tablename__ = 'guest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    traits = db.relationship("Trait", uselist=False, backref="guest_traits")
    requirements = db.relationship("Trait", uselist=False, backref="guest_requirements")
    def process_traits(self, data):
        for key, value in data.items():
            setattr(self.traits, key, value)
        return True
    def process_requirements(self, data):
        for key, value in data.items():
            setattr(self.requirements, key, value)
        return True
