from . import SafeHouseTesting
from v1.apps import db

from v1.apps.users.models import User
from v1.apps.safehouse.hosts.models import Suspend
from v1.apps.safehouse.models import Trait

from datetime import date

class DBTests(SafeHouseTesting):
    def test_user_login(self):
        username = "TestUser1"
        correct_password = "password"
        incorrect_password = "Password"
        user = User.query.filter_by(username=username).first()
        assert username in user.username
        assert user.verify_password(correct_password)
        assert not user.verify_password(incorrect_password)
        assert user.guest is not None

    def test_availability(self):
        user = User.query.get(12)
        user.host.suspended_dates.append(Suspend(from_date=date(2017,6,1), to_date=date(2017,6,14)))
        user.host.suspended_dates.append(Suspend(from_date=date(2017,10,5), to_date=date(2017,10,6)))
        assert user.host.is_available(date(2017,6,4)) == False
        assert user.host.is_available(date(2017,6,15)) == True
        assert user.host.is_available(date(2017,10,5)) == False

    def test_match(self):
        guest_smoker = User.query.get(3).guest
        guest_smoker.traits = Trait(smoker=True)
        db.session.add(guest_smoker)
        host_nonsmoker = User.query.get(12).host
        host_nonsmoker.requirements = Trait(smoker=False)
        db.session.add(host_nonsmoker)
        host_smoker = User.query.get(17).host
        host_smoker.requirements = Trait(smoker=True)
        db.session.add(host_smoker)
        db.session.commit()
        assert guest_smoker.traits.smoker == host_smoker.requirements.smoker
        assert guest_smoker.traits.smoker != host_nonsmoker.requirements.smoker
