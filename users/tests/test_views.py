
from django.test import TestCase
from django.urls import resolve

from users.views import index, user_login
from users.models import UserProfile


class IndexViewTest(TestCase):

    def test_index_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_renders_by_correct_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, "index.html")


class LoginViewTest(TestCase):

    def test_login_url_resolve(self):
        found = resolve('/login/')
        self.assertEqual(found.func, user_login)

    def test_login_url_GET_correct_template(self):
        resp = self.client.get('/login/')
        self.assertTemplateUsed(resp, "login.html")

    def test_login_url_POST_to_existing_user(self):
        user = UserProfile.objects.create(username="test", password="123456abc", email="test@test.com")
        resp = self.client.post('/login/', data={
            "username": "test",
            "password": "123456abc",
        })
        # TODO: 不能测试用户登陆
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "index.html")
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
