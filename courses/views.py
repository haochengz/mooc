
from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course


class CourseListView(View):

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_courses = Course.objects.all().order_by("-hits")
            elif sort == "students":
                all_courses = Course.objects.all().order_by("-enrolled_nums")
            else:
                all_courses = Course.objects.all().order_by("-add_time")
        else:
            all_courses = Course.objects.all().order_by("-add_time")

        paginator = Paginator(all_courses, 8, request=request)
        courses = paginator.page(page)
        return render(request, "course-list.html", {
            "courses": courses,
            "sort": sort,
        })
