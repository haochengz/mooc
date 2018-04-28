
from django.test import TestCase
from django.urls import resolve

from organizations.views import OrgListView
from organizations.models import Org, Location


class OrgListViewTest(TestCase):

    def setUp(self):
        beijing = Location.objects.create(
            name="Beijing",
        )
        Org.objects.create(
            name="Peiking University",
            category="college",
            located=beijing,
        )
        Org.objects.create(
            name="Tsinghua University",
            category="college",
            located=beijing,
        )

    def test_resolve_org_index_url(self):
        found = resolve("/orgs/")
        self.assertEqual(found.func.view_class, OrgListView)

    def test_template_used_correct_at_org_list_url(self):
        resp = self.client.get("/orgs/")
        self.assertTemplateUsed(resp, "org-list.html")

    def test_org_list_page_shows_organizations_from_db(self):
        resp = self.client.get('/orgs/')
        self.assertContains(resp, "Peiking University")
        self.assertContains(resp, "Tsinghua University")

    def test_org_list_page_shows_cities_from_db(self):
        resp = self.client.get('/orgs/')
        self.assertContains(resp, 'Beijing')
        self.assertNotContains(resp, 'Tibet')
