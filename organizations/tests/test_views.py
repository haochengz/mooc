
from django.test import TestCase
from django.urls import resolve

from organizations.views import OrgListView


class OrgListViewTest(TestCase):

    def test_resolve_org_index_url(self):
        found = resolve("/orgs/")
        self.assertEqual(found.func.view_class, OrgListView)

    def test_template_used_correct_at_org_list_url(self):
        resp = self.client.get("/orgs/")
        self.assertTemplateUsed(resp, "org-list.html")
