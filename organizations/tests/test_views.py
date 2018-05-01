
from django.test import TestCase
from django.urls import resolve

from organizations.views import (
    OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView,
    AddFavView,
)
from organizations.models import Org, Location, Instructor
from courses.models import Course


class OrgListViewAndUserConsultViewTest(TestCase):

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

    def test_sort_orgs_by_course_nums(self):
        resp = self.client.get('/orgs/')
        self.assertNotContains(resp, 'Fudan University')
        self.assertNotContains(resp, 'iMooc.com')

        resp = self.client.get('/orgs/', {'sort': 'courses'})
        self.assertContains(resp, 'Fudan University')
        self.assertContains(resp, 'iMooc.com')

    def test_sort_orgs_by_students_nums(self):
        resp = self.client.get('/orgs/')
        self.assertNotContains(resp, 'Fudan University')
        self.assertNotContains(resp, 'iMooc.com')

        resp = self.client.get('/orgs/', {'sort': 'students'})
        self.assertContains(resp, 'Fudan University')
        self.assertContains(resp, 'iMooc.com')

    def test_submit_a_consulation_to_db(self):
        self.client.post('/orgs/consult/', data={
            "name": "WuHong Wang",
            "mobile": "13888777666",
            "course_name": "Introduction to Python",
        })

        from operations.models import UserConsult
        consult = UserConsult.objects.get(name='WuHong Wang')
        self.assertEqual(consult.mobile, '13888777666')

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
            hits=700,
            enrolled_nums=700,
        )
        Org.objects.create(
            name="University of C",
            category="college",
            located=beijing,
            hits=600,
            enrolled_nums=600,
        )
        Org.objects.create(
            name="University of D",
            category="college",
            located=beijing,
            hits=500,
            enrolled_nums=500,
        )
        Org.objects.create(
            name="University of E",
            category="college",
            located=shanghai,
            hits=400,
            enrolled_nums=400,
        )
        Org.objects.create(
            name="J.C. Michael",
            category="personal",
            located=shanghai,
            hits=300,
            enrolled_nums=2000,
            course_nums=300,
        )
        Org.objects.create(
            name="iMooc.com",
            category="vocational",
            located=shanghai,
            hits=200,
            enrolled_nums=2100,
            course_nums=200,
        )
        Org.objects.create(
            name="Fudan University",
            category="college",
            located=shanghai,
            hits=100,
            enrolled_nums=2200,
            course_nums=100,
        )


class OrgViewTest(TestCase):
    """
    Test case for OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
    """

    def setUp(self):
        beijing = Location.objects.create(
            name="Beijing",
        )
        self.pku = Org.objects.create(
            name="Peiking University",
            category="college",
            located=beijing,
            hits=1000,
            enrolled_nums=1000,
        )
        self.thu = Org.objects.create(
            name="Tsinghua University",
            category="college",
            located=beijing,
            hits=900,
            enrolled_nums=900,
        )
        self.create_courses()
        self.create_teachers()

    def test_resolve_org_home_correct(self):
        found = resolve('/orgs/home/%d/' % self.pku.id)
        self.assertEqual(found.func.view_class, OrgHomeView)

    def test_resolve_org_course_correct(self):
        found = resolve('/orgs/course/%d/' % self.pku.id)
        self.assertEqual(found.func.view_class, OrgCourseView)

    def test_resolve_org_desc_correct(self):
        found = resolve('/orgs/desc/%d/' % self.pku.id)
        self.assertEqual(found.func.view_class, OrgDescView)

    def test_resolve_org_teacher_correct(self):
        found = resolve('/orgs/teacher/%d/' % self.pku.id)
        self.assertEqual(found.func.view_class, OrgTeacherView)

    def test_org_home_uses_org_homepage_template(self):
        resp = self.client.get('/orgs/home/%d/' % self.pku.id)
        self.assertTemplateUsed(resp, 'org-detail-homepage.html')

    def test_org_home_uses_org_course_template(self):
        resp = self.client.get('/orgs/course/%d/' % self.pku.id)
        self.assertTemplateUsed(resp, 'org-detail-course.html')

    def test_org_home_uses_org_desc_template(self):
        resp = self.client.get('/orgs/desc/%d/' % self.pku.id)
        self.assertTemplateUsed(resp, 'org-detail-desc.html')

    def test_org_home_uses_org_teacher_template(self):
        resp = self.client.get('/orgs/teacher/%d/' % self.pku.id)
        self.assertTemplateUsed(resp, 'org-detail-teachers.html')

    def test_org_home_page_display_the_course_belong_to_the_orgs(self):
        resp = self.client.get('/orgs/home/%d/' % self.pku.id)
        self.assertContains(resp, "Introduction to Python")
        self.assertNotContains(resp, "Introduction to Compiler")

    def test_org_home_page_displays_the_teachers_belong_to_the_orgs(self):
        resp = self.client.get('/orgs/home/%d/' % self.pku.id)
        self.assertContains(resp, "Ms. Zhou")
        self.assertNotContains(resp, "Dr. Zhao")

    def create_courses(self):
        Course.objects.create(
            name="Introduction",
            desc="",
            degree="junior",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.pku,
        )
        Course.objects.create(
            name="Introduction to Python",
            desc="",
            degree="junior",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.pku,
        )
        Course.objects.create(
            name="Introduction to Operating System",
            desc="",
            degree="senior",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.pku,
        )
        Course.objects.create(
            name="Introduction to Compiler",
            desc="",
            degree="senior",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.thu,
        )
        Course.objects.create(
            name="Introduction to Network",
            desc="",
            degree="expert",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.pku,
        )
        Course.objects.create(
            name="Introduction to Database",
            desc="",
            degree="expert",
            detail="",
            duration_mins=300,
            enrolled_nums=1000,
            favorite_nums=1000,
            hits=10000,
            org=self.thu,
        )

    def create_teachers(self):
        Instructor.objects.create(
            name="Ms. Zhou",
            org=self.pku
        )
        Instructor.objects.create(
            name="Pr. Wang",
            org=self.pku
        )
        Instructor.objects.create(
            name="Pr. Liu",
            org=self.thu
        )
        Instructor.objects.create(
            name="Dr. Zhao",
            org=self.thu
        )


class AddFavViewTest(TestCase):

    def test_resolve_correct_to_add_fav(self):
        found = resolve('/orgs/add_fav/')
        self.assertEqual(found.func.view_class, AddFavView)

    def test_when_user_was_not_login_should_return_failed_json(self):
        resp = self.client.post('/orgs/add_fav/', data={
            "": "",
        })




