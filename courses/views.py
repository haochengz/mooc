
from django.views.generic import View
from django.shortcuts import render

from .models import Course


class CourseListView(View):

    @staticmethod
    def get(request):
        all_courses = Course.objects.all()
        return render(request, "course-list.html", {
            "all_courses": all_courses,
        })
