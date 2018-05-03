
from django.urls import resolve
from django.test import TestCase

from courses.views import CourseListView


class CourseListViewTest(TestCase):

    def test_resolve_url_correct(self):
        found = resolve("/course/list/")
        self.assertEqual(found.func.view_class, CourseListView)

    def test_render_correct_template(self):
        resp = self.client.get("/course/list/")
        self.assertTemplateUsed(resp, "course-list.html")
