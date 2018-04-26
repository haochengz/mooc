
from django.test import TestCase
from django.urls import resolve

from organizations.views import OrgListView


class OrgListViewTest(TestCase):

    def test_resolve_org_index_url(self):
        found = resolve("/org-list/")
        self.assertEqual(found.func.view_class, OrgListView)
