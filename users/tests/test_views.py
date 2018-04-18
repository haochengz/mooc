
from django.test import TestCase
from django.urls import resolve

from users.views import index, user_login


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
