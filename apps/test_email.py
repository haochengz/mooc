
from django.test import TestCase

from apps.utils.email import send_register_verify_mail, generate_random_code, generate_register_mail, generate_verify_url
from users.models import UserProfile
from users.models import EmailVerify
from local import server_url


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

    def test_generate_random_code(self):
        code = generate_random_code()
        self.assertEqual(len(code), 32)

    def test_generate_register_mail(self):
        code = generate_random_code()
        subject, text = generate_register_mail(code)

        self.assertEqual(subject, "Mooc verify mail")
        self.assertIn(code, text)

    def test_generate_mail(self):
        code = generate_random_code()
        url = generate_verify_url(code)
        self.assertIn(code, url)
        self.assertEqual(url, server_url + "activate/" + code + '/')

    def test_no_repetitive_code_in_db(self):
        send_register_verify_mail(user=self.user)
        email_verify_recode = EmailVerify.objects.get(email=self.user.email)
        res = EmailVerify.objects.filter(code=email_verify_recode.code)
        self.assertEqual(len(res), 1)

    def test_never_had_a_repetition_verify_code(self):
        # Unable to test
        pass

