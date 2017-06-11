from . import SafeHouseTesting
from v1.apps.users.models import User
from v1.apps.safehouse.hosts.models import Suspend

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
        if user.guest is not None:
            print(user.guest.trait.language)
        username = "TestUser12"
        correct_password = "password"
        incorrect_password = "Password"
        user = User.query.filter_by(username=username).first()
        if user.host is not None:
            user.host.suspended_dates.append(Suspend(from_date=date(2017,10,5), to_date=date(2017,10,6)))
            assert user.host.is_available(date(2017,6,4)) == False
            assert user.host.is_available(date(2017,6,15)) == True
            assert user.host.is_available(date(2017,10,5)) == False
