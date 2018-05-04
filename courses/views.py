
from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, Resource


class CourseListView(View):

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        sort = request.GET.get("sort", "")
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-hits")[:3]
        if sort:
            if sort == "hot":
                all_courses = Course.objects.all().order_by("-hits")
            elif sort == "students":
                all_courses = Course.objects.all().order_by("-enrolled_nums")

        paginator = Paginator(all_courses, 8, request=request)
        courses = paginator.page(page)
        return render(request, "course-list.html", {
            "courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
        })


class CourseDetailView(View):

    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=course_id)
        course.hits += 1
        course.save()

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag).exclude(id=course_id)[:1]
        else:
            related_courses = []

        return render(request, "course-detail.html", {
            "course": course,
            "related_courses": related_courses,
        })

    # TODO: Categorize by tag
    # TODO: Fav the course and org at the course detail page


class CourseInfoView(View):

    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=course_id)
        resources = Resource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": resources,
        })
