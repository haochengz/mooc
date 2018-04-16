from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from .models import UserProfile


class UserProfileTest(TestCase):

    def test_userprofile_saving_and_retrieving_from_db(self):
        john = UserProfile(
            username="john",
            password="123456",
            first_name="John",
            last_name="Dow",
            email="johndow@gmail.com",
            is_staff=True,
            is_active=False,
            date_joined=timezone.now(),
            nick_name="strider",
            birthday=datetime(1988, 3, 28),
            gender="male",
            address="No.7 Euclid St. Mountain View, San Francisco, CA, USA",
            mobile="550(425)8809",
            image="media/image/default.png",
        )
        jim = UserProfile(
            username="jim",
            password="123456",
            first_name="jim",
            last_name="Dow",
            email="jimdoug@gmail.com",
            is_staff=True,
            is_active=False,
            date_joined=timezone.now(),
            nick_name="bear",
            birthday=datetime(1988, 3, 28),
            gender="male",
            address="No.8 Euclid St. Mountain View, San Francisco, CA, USA",
            mobile="550(425)3536",
            image="media/image/default.png",
        )
        john.save()
        jim.save()

        saved_users = UserProfile.objects.all()
        self.assertEqual(saved_users.count(), 2)
        self.assertEqual(john.username, saved_users[0].username)
        self.assertEqual(jim.username, saved_users[1].username)
