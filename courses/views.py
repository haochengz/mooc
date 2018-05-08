
from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse

from .models import Course, Resource, Section
from operations.models import CourseComment, UserCourse
from apps.utils.tools import LoginRequiredMixin


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
            related_courses = Course.objects.filter(tag=tag).exclude(id=course_id)[:3]
        else:
            related_courses = []

        return render(request, "course-detail.html", {
            "course": course,
            "related_courses": related_courses,
        })
    # TODO(haochengz@outlook.com): test render, resolve, related_courses


class CourseInfoView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=course_id)
        resources = Resource.objects.filter(course=course)
        user = request.user

        already_enrolled = UserCourse.objects.filter(course=course, user=user)
        if not len(already_enrolled):
            UserCourse.objects.create(
                course=course,
                user=user,
            )
            course.enrolled_nums += 1
            course.save()

        user_courses = UserCourse.objects.filter(course=course)
        courses_id = [uc.course.id for uc in user_courses]
        relate_courses = Course.objects.filter(id__in=courses_id).order_by("-hits")[:3]
        # TODO: need refactor here
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": resources,
            "relate_courses": relate_courses,
        })

    # TODO(haochengz@outlook.com): test render, resolve, related_courses, course.enrolled_nums modifiers in db


class CommentView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=course_id)
        resources = Resource.objects.filter(course=course)
        comments = CourseComment.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": resources,
            "comments": comments,
        })
    # TODO(haochengz@outlook.com): test render, resolve, comments from db, need login


class AddCommentView(View):

    @staticmethod
    def post(request):
        user = request.user
        if user.is_authenticated:
            course_id = request.POST.get("course_id", 0)
            comment = request.POST.get("comments", "")
            if course_id == 0 or comment == "":
                return HttpResponse("{'status': 'fail', 'message': 'Failed'}")
            CourseComment.objects.create(
                user=user,
                course=Course.objects.get(id=course_id),
                comment=comment,
            )
            return HttpResponse("{'status': 'success', 'message': 'Success'}")
        return HttpResponse("{'status': 'fail', 'message': 'Failed'}")
    # TODO(haochengz@outlook.com): test render, resolve, add comments to db, maybe failed, need login


class VideoPlayView(View):

    @staticmethod
    def get(request, video_id):
        video = Section.objects.get(id=video_id)
        course = video.chapter.course
        resources = Resource.objects.filter(course=course)

        # TODO: 查询是否已经关联该课程, 未关联则建立连接

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [uc.user.id for uc in user_courses]
        all_uc = UserCourse.objects.filter(user_id__in=user_ids)
        courses_id = [uc.course.id for uc in user_courses]
        relate_courses = Course.objects.filter(id__in=courses_id).order_by("-hits")[:3]
        # TODO: need refactor here
        return render(request, "course-play.html", {
            "course": course,
            "course_resources": resources,
            "relate_courses": relate_courses,
            "video": video,
        })

    # TODO(haochengz@outlook.com): test render, resolve, need login

