
from datetime import datetime

from django.test import TestCase
from django.urls import resolve
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate

from users.views import index, LoginView, RegisterView, ActivateUserView, ForgetView, RetrievePasswordView, ModifyView
from users.models import UserProfile, EmailVerify
from apps.utils.email import generate_verify_url, generate_retrieve_url
from apps.utils.tools import minutes_ago


class IndexViewTest(TestCase):

    def test_index_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_renders_by_correct_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, "index.html")


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = UserProfile(username="test", email="test@tests.com")
        self.user.set_password("123456abc")
        self.user.save()

    def test_login_url_resolve(self):
        found = resolve('/login/')
        self.assertEqual(found.func.view_class, LoginView)

    def test_login_url_GET_correct_template(self):
        resp = self.client.get('/login/')
        self.assertTemplateUsed(resp, "login.html")

    def test_login_url_POST_to_existing_user(self):
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "123456abc",
        })

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "index.html")
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    def test_login_with_POST_wrong_username_or_password_should_return_to_login_page(self):
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "123456",
        })

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

        resp = self.client.post('/login/', data={
            "username": "test1",
            "password": "123456abc",
        })

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_only_activated_user_login(self):
        user = UserProfile(username="unactivated", email="unactivated@tests.com", is_active=False)
        user.set_password("123456abc")
        user.save()
        resp = self.client.post('/login/', data={
            "username": "unactivated",
            "password": "123456abc",
        })

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "user unactivated is not activated")

    def test_login_with_POST_using_email_as_username_should_works_just_fun(self):
        resp = self.client.post('/login/', data={
            "username": "test@tests.com",
            "password": "123456abc",
        })

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "index.html")
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    def test_login_with_POST_return_to_login_page_and_given_a_error_msg(self):
        resp = self.client.post('/login/', data={
            "username": "test@tests.com",
            "password": "123456abb",
        })

        self.assertContains(resp, "invalid username or password")

    def test_login_with_empty_username_POST_should_be_fail(self):
        resp = self.client.post('/login/', data={
            "username": "",
            "password": "123456abc",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "这个字段是必须的")

    def test_login_with_empty_password_POST_should_be_fail(self):
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "这个字段是必须的")

    def test_login_POST_username_must_more_than_4_chars(self):
        resp = self.client.post('/login/', data={
            "username": "tes",
            "password": "123456abc",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "确保该变量至少包含")

    def test_login_POST_password_must_more_than_8_chars(self):
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "1234567",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "确保该变量至少包含")

    def test_login_POST_username_no_more_than_32_chars(self):
        resp = self.client.post('/login/', data={
            "username": "abcdefgjiuhgdsucjdkluehfngjchdjnf",
            "password": "123456abc",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "确保该变量包含不超过")

    def test_login_POST_password_no_more_than_16_chars(self):
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "12345678998765432",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "确保该变量包含不超过")


class RegisterViewTest(TestCase):

    def setUp(self):
        self.user = UserProfile(username="test", email="test@tests.com")
        self.user.set_password("123456abc")
        self.user.save()

    def test_register_url_resolve(self):
        found = resolve('/register/')
        self.assertEqual(found.func.view_class, RegisterView)

    def test_register_template_correct_when_asking_as_GET(self):
        resp = self.client.get('/register/')
        self.assertTemplateUsed(resp, 'register.html')

    def test_POST_a_user_register_request_to_view_then_create_user_in_db(self):
        captcha = self.captcha_through()
        resp = self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertTemplateUsed(resp, "login.html")
        self.assertIsNotNone(user)

    def test_POST_a_user_register_request_to_view_which_user_is_not_active(self):
        captcha = self.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertEqual(user.is_active, False)

    def test_POST_a_user_register_request_to_view_then_create_a_verify_code_in_db(self):
        captcha = self.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        verify_code = EmailVerify.objects.get(email="testuser@user.com")
        self.assertIsNotNone(verify_code)

    def test_POST_register_an_exists_email_should_reture_to_register_page(self):
        UserProfile.objects.create(
            username="testuser@user.com",
            email="testuser@user.com",
            password="123456789",
        )
        captcha = self.captcha_through()
        resp = self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        self.assertTemplateUsed(resp, "register.html")
        self.assertContains(resp, "email already exists")

    @staticmethod
    def captcha_through():
        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        return captcha


class ActivateViewTest(TestCase):

    def test_activate_url_resolve(self):
        found = resolve("/activate/some_validation_code/")
        self.assertEqual(found.func.view_class, ActivateUserView)

    def test_resend_verify_code_url_resolve(self):
        found = resolve('/reactive/')
        self.assertEqual(found.func.view_class, ActivateUserView)

    def test_activate_unactive_user(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        activate_url = generate_verify_url(record.code)
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "login.html")
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertTrue(user.is_active)

    def test_activate_unactive_user_with_a_wrong_active_code(self):
        activate_url = generate_verify_url("Hfjsdlfeur")
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "cannot activate user, active code is wrong")

    def test_validation_code_could_been_out_of_date(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        register_time = minutes_ago(datetime.now(), 31)
        record.send_time = register_time
        record.save()
        activate_url = generate_verify_url(record.code)
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "the validation code is out of date")
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertFalse(user.is_active)

    def test_delete_the_validation_code_once_it_has_been_verified(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        activate_url = generate_verify_url(record.code)
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "login.html")
        self.assertEqual(EmailVerify.objects.count(), 0)
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(len(record), 0)

    def test_delete_the_validation_code_once_it_has_been_expired(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        register_time = minutes_ago(datetime.now(), 31)
        record.send_time = register_time
        record.save()
        activate_url = generate_verify_url(record.code)
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "the validation code is out of date")
        self.assertEqual(EmailVerify.objects.count(), 0)
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(len(record), 0)

    def test_resend_a_validation_code_request_by_an_activated_user_should_return_wrong(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        activate_url = generate_verify_url(record.code)
        self.client.get(activate_url)
        resp = self.client.post("/reactive/", data={
            "email": "testuser@user.com",
        })

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "email address already been activated")
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertTrue(user.is_active)

    def test_resend_a_validation_code_by_an_un_register_email(self):
        resp = self.client.post("/reactive/", data={
            "email": "somedude@user.com",
        })

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "please register first")

    def test_only_re_send_the_validation_code_after_15_minutes_when_last_sent(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        register_time = minutes_ago(datetime.now(), 31)
        record.send_time = register_time
        record.save()
        self.client.post("/reactive/", data={
            "email": "testuser@user.com",
        })
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(record.count(), 2)
        activate_url = generate_verify_url(record[1].code)
        resp = self.client.get(activate_url)

        self.assertTemplateUsed(resp, "login.html")
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertTrue(user.is_active)

    def test_resend_a_request_to_have_a_new_validation_code_less_than_15_minutes_when_last_sent(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        resp = self.client.post("/reactive/", data={
            "email": "testuser@user.com",
        })
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(record.count(), 1)

        self.assertTemplateUsed(resp, "verify.html")
        self.assertContains(resp, "same email address only re-send a validation code every 15 minutes")
        user = UserProfile.objects.get(email="testuser@user.com")
        self.assertFalse(user.is_active)

    def test_resend_a_request_new_validation_code_less_than_15_minutes_when_and_only_last_sent(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "testuser@user.com",
            "password": "12345566",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })
        record = EmailVerify.objects.get(email="testuser@user.com")
        register_time = minutes_ago(datetime.now(), 15)
        record.send_time = register_time
        record.save()
        self.client.post("/reactive/", data={
            "email": "testuser@user.com",
        })
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(record.count(), 2)
        self.client.post("/reactive/", data={
            "email": "testuser@user.com",
        })
        record = EmailVerify.objects.filter(email="testuser@user.com")
        self.assertEqual(record.count(), 2)


class ForgetViewTest(TestCase):

    def setUp(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "user@testserver.com",
            "password": "12345678",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

    def test_forget_url_resolve(self):
        found = resolve("/forget/")
        self.assertEqual(found.func.view_class, ForgetView)

    def test_request_get_to_forget_page(self):
        resp = self.client.get('/forget/')
        self.assertTemplateUsed(resp, "forgetpwd.html")

    def test_post_a_request_to_get_a_retrieve_mail(self):
        captcha = RegisterViewTest.captcha_through()
        resp = self.client.post("/forget/", data={
            "email": "user@testserver.com",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

        validation_code_generated_at_db = EmailVerify.objects.filter(email="user@testserver.com")
        self.assertNotEqual(len(validation_code_generated_at_db), 0)
        self.assertTemplateUsed(resp, "index.html")

    def test_post_an_un_exists_user_to_forget(self):
        captcha = RegisterViewTest.captcha_through()
        resp = self.client.post("/forget/", data={
            "email": "user@someserver.com",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

        validation_code_generated_at_db = EmailVerify.objects.filter(email="user@someserver.com")
        self.assertEqual(len(validation_code_generated_at_db), 0)
        self.assertTemplateUsed(resp, "forgetpwd.html")
        self.assertContains(resp, "Wrong email address")


class RetrievePasswordTest(TestCase):

    def setUp(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "user@testserver.com",
            "password": "12345678",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

        captcha = RegisterViewTest.captcha_through()
        self.client.post("/forget/", data={
            "email": "user@testserver.com",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

    def test_retrieve_password_url_resolve(self):
        found = resolve("/retrieve/some-validation-code-here/")
        self.assertEqual(found.func.view_class, RetrievePasswordView)

    def test_retrieve_password_via_a_url_send_to_users_mail(self):
        records = EmailVerify.objects.filter(email="user@testserver.com", verify_type="forget")
        retrieve_url = generate_retrieve_url(records[0].code)
        resp = self.client.get(retrieve_url)

        self.assertTemplateUsed(resp, "password_reset.html")
        self.assertContains(resp, "user@testserver.com")

    def test_retrieve_password_via_a_wrong_code_should_be_fail(self):
        retrieve_url = generate_retrieve_url("an_absolute_wrong_validation_code")
        resp = self.client.get(retrieve_url)

        self.assertTemplateUsed(resp, "register.html")
        self.assertContains(resp, "Wrong validation code")

    def test_retrieve_password_via_a_out_of_date_validation_code(self):
        records = EmailVerify.objects.get(email="user@testserver.com", verify_type="forget")
        request_time = minutes_ago(datetime.now(), 31)
        records.send_time = request_time
        records.save()
        retrieve_url = generate_retrieve_url(records.code)
        resp = self.client.get(retrieve_url)

        self.assertTemplateUsed(resp, "register.html")
        self.assertContains(resp, "validation code out of date")

    def test_delete_out_of_date_validation_code(self):
        records = EmailVerify.objects.get(email="user@testserver.com", verify_type="forget")
        request_time = minutes_ago(datetime.now(), 31)
        records.send_time = request_time
        records.save()
        retrieve_url = generate_retrieve_url(records.code)
        resp = self.client.get(retrieve_url)

        self.assertTemplateUsed(resp, "register.html")
        self.assertContains(resp, "validation code out of date")
        self.assertEqual(EmailVerify.objects.filter(email="user@testserver.com", verify_type="forget").count(), 0)


class ModifyViewTest(TestCase):

    def setUp(self):
        captcha = RegisterViewTest.captcha_through()
        self.client.post("/register/", data={
            "email": "user@testserver.com",
            "password": "12345678",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

        captcha = RegisterViewTest.captcha_through()
        self.client.post("/forget/", data={
            "email": "user@testserver.com",
            "captcha_0": captcha.hashkey,
            "captcha_1": captcha.response,
        })

        records = EmailVerify.objects.filter(email="user@testserver.com", verify_type="forget")
        retrieve_url = generate_retrieve_url(records[0].code)
        self.client.get(retrieve_url)

    def test_modify_url_resolve(self):
        found = resolve("/modify/")
        self.assertEqual(found.func.view_class, ModifyView)

    def test_reset_a_new_password(self):
        resp = self.client.post("/modify/", data={
            "pwd1": "987654321",
            "pwd2": "987654321",
            "email": "user@testserver.com",
        })

        self.assertTemplateUsed(resp, "login.html")
        self.assertContains(resp, "reset success, please login")
        self.assertTrue(authenticate(username="user@testserver.com", password="987654321"))

    def test_reset_with_wrong_input(self):
        resp = self.client.post("/modify/", data={
            "pwd1": "9876543210",
            "pwd2": "987654321",
            "email": "user@testserver.com",
        })

        self.assertTemplateUsed(resp, "password_reset.html")
        self.assertFalse(authenticate(username="user@testserver.com", password="987654321"))
