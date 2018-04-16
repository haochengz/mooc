from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from .models import UserProfile, EmailVerify, Banner


class UserModuleModelsDBConnectionTest(TestCase):

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
            gender="female",
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

    def test_emailverify_saving_and_retrieving_from_db(self):
        register_code = EmailVerify(
            code="123456",
            email="jim@gmail.com",
            verify_type="register",
            send_time=timezone.now(),
        )
        forget_code = EmailVerify(
            code="654321",
            email="hype@gmail.com",
            verify_type="forget",
            send_time=timezone.now(),
        )
        register_code.save()
        forget_code.save()

        codes = EmailVerify.objects.all()
        self.assertEqual(codes.count(), 2)
        self.assertEqual(codes[0].code, register_code.code)
        self.assertEqual(codes[1].code, forget_code.code)

    def test_banner_saving_and_retrieving_from_db(self):
        google = Banner(
            title="Google News Initial",
            image="media/banner/2018/04",
            url="https://news.google.com",
            index=9000,
            add_time=timezone.now(),
        )
        amazon = Banner(
            title="Kindle Sales",
            image="media/banner/2018/04",
            url="https://amazon.com",
            index=11000,
            add_time=timezone.now(),
        )
        google.save()
        amazon.save()

        banners = Banner.objects.all()
        self.assertEqual(banners.count(), 2)
        self.assertEqual(banners[0].title, "Google News Initial")
        self.assertEqual(banners[1].title, "Kindle Sales")
