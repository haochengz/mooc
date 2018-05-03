
from django.urls import resolve
from django.test import TestCase

from courses.views import CourseListView, CourseDetailView
from courses.models import Course, Chapter
from users.models import UserProfile
from operations.models import UserCourse
from organizations.models import Org, Location, Instructor


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
        compiler = Course.objects.create(
            name="Compiler",
            duration_mins=300,
            hits=10000,
            enrolled_nums=300,
            category="CS",
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
        Chapter.objects.create(
            name="Introduction",
            course=compiler,
        )
        Chapter.objects.create(
            name="tokenize",
            course=compiler,
        )
        user = UserProfile.objects.create(
            username="user",
            email="user@server.com",
        )
        UserCourse.objects.create(
            user=user,
            course=compiler,
        )
        Instructor.objects.create(
            name="Pr. Zhang",
            org=stanford,
        )

    def test_resolve_correct(self):
        found = resolve("/course/detail/1/")
        self.assertEqual(found.func.view_class, CourseDetailView)

    def test_template_render_correct(self):
        resp = self.client.get("/course/detail/1/")
        self.assertTemplateUsed(resp, "course-detail.html")

    def test_shows_the_detail_of_the_course(self):
        resp = self.client.get("/course/detail/1/")
        self.assertContains(resp, "Compiler")

    def test_shows_how_many_students_were_leaning_this_course(self):
        resp = self.client.get("/course/detail/1/")
        self.assertContains(resp, "学习人数：1")

    def test_shows_how_many_chapters_of_this_course(self):
        resp = self.client.get("/course/detail/1/")
        self.assertContains(resp, "章&nbsp;节&nbsp;数：</span><span>2")

    def test_shows_the_orgs_on_the_right_side_of_the_page(self):
        resp = self.client.get("/course/detail/1/")
        self.assertContains(resp, "Stanford University")

    def test_shows_some_detail_of_the_org(self):
        resp = self.client.get("/course/detail/1/")
        course_num_str = "<span>课 &nbsp;程&nbsp; 数：&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   %d</span>" % 0
        self.assertContains(resp, course_num_str)

        teacher_num_str = "<span>教 &nbsp;师&nbsp; 数：&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  %d</span>" % 1
        self.assertContains(resp, teacher_num_str)
