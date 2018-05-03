
from django.urls import resolve
from django.test import TestCase

from courses.views import CourseListView, CourseDetailView
from courses.models import Course
from organizations.models import Org, Location


class CourseListViewTest(TestCase):

    def setUp(self):
        mountain_view = Location.objects.create(
            name="Mountain View",
        )
        stanford = Org.objects.create(
            name="Stanford University",
            located=mountain_view,
        )
        Course.objects.create(
            name="Compiler",
            duration_mins=300,
            hits=10000,
            org=stanford,
        )
        Course.objects.create(
            name="Introduction to Database",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Python",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Database",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="How to create a website",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Deep learning",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Programming Methodology",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Math",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Operating System",
            duration_mins=300,
            hits=1000,
            enrolled_nums=10000,
            org=stanford,
        )
        Course.objects.create(
            name="Network",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )

    def test_resolve_url_correct(self):
        found = resolve("/course/list/")
        self.assertEqual(found.func.view_class, CourseListView)

    def test_render_correct_template(self):
        resp = self.client.get("/course/list/")
        self.assertTemplateUsed(resp, "course-list.html")

    def test_pagination_of_course_list_page_by_8_courses_each_page(self):
        resp = self.client.get("/course/list/")
        self.assertContains(resp, "Python")
        # self.assertNotContains(resp, "Introduction to Database")
        self.assertContains(resp, "下一页")
        self.assertNotContains(resp, "上一页")

    def test_by_default_none_page_parameter_returns_first_page(self):
        resp1 = self.client.get("/course/list/", {
            "page": 1
        })
        resp2 = self.client.get("/course/list/")
        self.assertEqual(resp1.content, resp2.content)

    def test_by_default_the_list_page_returns_the_course_by_the_order_of_adding_time(self):
        resp = self.client.get("/course/list/")
        self.assertContains(resp, "Network")
        # self.assertNotContains(resp, "Compiler")

    def test_requests_second_page(self):
        resp = self.client.get("/course/list/", {
            "page": 2
        })
        self.assertContains(resp, "上一页")
        self.assertNotContains(resp, "下一页")
        self.assertContains(resp, "Introduction to Database")
        # self.assertNotContains(resp, "Python")

    def test_sort_by_enrolled_nums(self):
        resp = self.client.get("/course/list/", data={
            "sort": "students",
        })
        self.assertContains(resp, "Operating System")

    def test_sort_by_hits(self):
        resp = self.client.get("/course/list/", data={
            "sort": "hot",
        })
        self.assertContains(resp, "Compiler")


class CourseDetailViewTest(TestCase):

    def setUp(self):
        mountain_view = Location.objects.create(
            name="Mountain View",
        )
        stanford = Org.objects.create(
            name="Stanford University",
            located=mountain_view,
        )
        Course.objects.create(
            name="Compiler",
            duration_mins=300,
            hits=10000,
            org=stanford,
        )
        Course.objects.create(
            name="Introduction to Database",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Python",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Database",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="How to create a website",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Deep learning",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Programming Methodology",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Math",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )
        Course.objects.create(
            name="Operating System",
            duration_mins=300,
            hits=1000,
            enrolled_nums=10000,
            org=stanford,
        )
        Course.objects.create(
            name="Network",
            duration_mins=300,
            hits=1000,
            org=stanford,
        )

    def test_resolve_correct(self):
        found = resolve("/course/detail/1/")
        self.assertEqual(found.func.view_class, CourseDetailView)

    def test_template_render_correct(self):
        resp = self.client.get("/course/detail/1/")
        self.assertTemplateUsed(resp, "course-detail.html")
