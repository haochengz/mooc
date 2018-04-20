
from django.test import TestCase

from utils.email import send_register_verify_mail
from users.models import UserProfile
from users.models import EmailVerify


class EmailVerifyTest(TestCase):

    def setUp(self):
        self.user = UserProfile(
            username="hczhao",
            email="haochengzhao@outlook.com",
            password="123456"
        )
        self.user.save()

    def test_save_verify_code_record_to_database(self):
        email = self.user.email
        send_register_verify_mail(self.user)
        record = EmailVerify.objects.get(email=email)
        self.assertIsNotNone(record)

    def test_send_mail_to_user(self):
        status = send_register_verify_mail(self.user)
        self.assertTrue(status)
