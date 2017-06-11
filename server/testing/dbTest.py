from . import PartyCrawlTesting
from collections import Counter

from v1.apps.users.models import User

class PartyCrawlTesting(WWTesting):
    def user_login(self):
        username = "TestUser1"
        correct_password = "password"
        incorrect_password = "Password"
        user = User.query.filter_by(username=username).first()
        assert username in user.username
        assert user.verify_password(correct_password)
        assert not user.verify_password(incorrect_password)
