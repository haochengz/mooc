
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
            hits=1000,
            enrolled_nums=1000,
        )
        Org.objects.create(
            name="Tsinghua University",
            category="college",
            located=beijing,
            hits=900,
            enrolled_nums=900,
        )

        self.create_orgs()

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

    def test_org_list_page_shows_total_orgs_nums(self):
        resp = self.client.get('/orgs/')
        c = '<div class="all">共<span class="key">%d</span>家</div>' % Org.objects.count()
        self.assertContains(resp, c)

    def test_pagination_works(self):
        resp = self.client.get('/orgs/')
        self.assertTemplateUsed(resp, 'org-list.html')
        c = '<div class="all">共<span class="key">%d</span>家</div>' % Org.objects.count()
        self.assertContains(resp, c)

        self.assertContains(resp, '下一页')
        self.assertNotContains(resp, '上一页')

    def test_pagination_and_follow_to_next_page(self):
        resp = self.client.get('/orgs/', {'page': 1})
        self.assertTemplateUsed(resp, 'org-list.html')
        self.assertContains(resp, '下一页')
        self.assertNotContains(resp, '上一页')

        resp = self.client.get('/orgs/', {'page': 2})
        self.assertTemplateUsed(resp, 'org-list.html')
        self.assertNotContains(resp, '下一页')
        self.assertContains(resp, '上一页')

    def test_pagination_with_wrong_page_number_always_returns_first_page(self):
        resp = self.client.get('/orgs/', {'page': 1101})
        self.assertTemplateUsed(resp, 'org-list.html')
        self.assertContains(resp, '下一页')
        self.assertNotContains(resp, '上一页')

        resp = self.client.get('/orgs/')
        self.assertTemplateUsed(resp, 'org-list.html')
        self.assertContains(resp, '下一页')
        self.assertNotContains(resp, '上一页')

    def test_sift_by_city(self):
        beijing = Location.objects.get(name='Beijing')
        resp = self.client.get('/orgs/', {'page': 1, 'city': beijing.id})

        self.assertNotContains(resp, 'Fudan University')
        self.assertNotContains(resp, '上一页')
        self.assertNotContains(resp, '下一页')

    def test_sift_by_category(self):
        resp = self.client.get('/orgs/', {'page': 1, 'ct': "college"})

        self.assertContains(resp, 'Fudan University')
        self.assertNotContains(resp, 'WuHong Wang')
        self.assertNotContains(resp, '上一页')
        self.assertNotContains(resp, '下一页')

    def test_sift_by_city_and_category(self):
        shanghai = Location.objects.get(name='Shanghai')
        resp = self.client.get('/orgs/', {'page': 1, 'ct': "vocational", 'city': shanghai.id})

        self.assertNotContains(resp, 'WuHong Wang')
        self.assertNotContains(resp, 'Fudan University')
        self.assertNotContains(resp, 'J.C. Michael')
        self.assertContains(resp, 'iMooc.com')
        self.assertNotContains(resp, '上一页')
        self.assertNotContains(resp, '下一页')

    def test_display_a_ranking_board_at_the_right(self):
        shanghai = Location.objects.get(name='Shanghai')
        resp = self.client.get('/orgs/', {'page': 1, 'ct': "personal", 'city': shanghai.id})

        self.assertContains(resp, "Peiking University")
        self.assertContains(resp, "Tsinghua University")
        self.assertContains(resp, "Beijing Tranning School")

    @staticmethod
    def create_orgs():
        beijing = Location.objects.get(name="Beijing")
        shanghai = Location.objects.create(
            name="Shanghai"
        )
        Org.objects.create(
            name="Beijing Tranning School",
            category="vocational",
            located=beijing,
            hits=800,
            enrolled_nums=800,
        )
        Org.objects.create(
            name="WuHong Wang",
            category="personal",
            located=beijing,
        )
        Org.objects.create(
            name="University of C",
            category="college",
            located=beijing,
        )
        Org.objects.create(
            name="University of D",
            category="college",
            located=beijing,
        )
        Org.objects.create(
            name="University of E",
            category="college",
            located=shanghai,
        )
        Org.objects.create(
            name="J.C. Michael",
            category="personal",
            located=shanghai,
        )
        Org.objects.create(
            name="iMooc.com",
            category="vocational",
            located=shanghai,
        )
        Org.objects.create(
            name="Fudan University",
            category="college",
            located=shanghai,
        )

