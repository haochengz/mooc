
from django.test import TestCase
from django.urls import resolve
from django.db import IntegrityError
from captcha.models import CaptchaStore

from users.views import index, LoginView, RegisterView
from users.models import UserProfile, EmailVerify


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
        # user = UserProfile.objects.get(email="testuser@user.com")
        self.assertTemplateUsed(resp, "login.html")
        # self.assertIsNotNone(user)

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

    def test_POST_a_user_register_request_to_view_which_is_already_in_db_should_raise_IntegrityError(self):
        UserProfile.objects.create(
            username = "testuser@user.com",
            email="testuser@user.com",
            password="123456789",
        )
        with self.assertRaises(IntegrityError) as e:
            captcha = self.captcha_through()
            self.client.post("/register/", data={
                "email": "testuser@user.com",
                "password": "12345566",
                "captcha_0": captcha.hashkey,
                "captcha_1": captcha.response,
            })
        self.assertEqual(e.exception.args[0], "UNIQUE constraint failed: users_userprofile.username")

    @staticmethod
    def captcha_through():
        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        return captcha

