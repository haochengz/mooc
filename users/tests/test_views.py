
from django.test import TestCase
from django.urls import resolve

from users.views import index, LoginView
from users.models import UserProfile


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
