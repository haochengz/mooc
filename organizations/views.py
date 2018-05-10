
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Org, Location, Instructor
from operations.models import UserFavorite
from .forms import UserConsultForm
from apps.utils.tools import add_favorite


class OrgListView(View):

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        sort_by = request.GET.get('sort', '')

        all_cities = Location.objects.all()
        all_orgs = Org.objects.all()
        top_orgs = all_orgs.order_by("-hits")[:3]

        if city_id:
            all_orgs = all_orgs.filter(located_id=city_id)
        if category:
            all_orgs = all_orgs.filter(category=category)
        if sort_by:
            if sort_by == "students":
                all_orgs = all_orgs.order_by("-enrolled_nums")
            elif sort_by == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        paginator = Paginator(all_orgs, 8, request=request)
        orgs = paginator.page(page)
        return render(request, "org-list.html", {
            "orgs": orgs,
            "all_cities": all_cities,
            "org_nums": all_orgs.count(),
            "city_id": city_id,
            "category": category,
            "top_orgs": top_orgs,
            "sort": sort_by,
        })


class UserConsultView(View):

    @staticmethod
    def post(request):
        consult = UserConsultForm(request.POST)
        if consult.is_valid():
            consult.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        return HttpResponse("{'status': 'failed', 'msg': 'Failed'}", content_type='application/json')

    # FIXME: org-list js didn't work


class OrgHomeView(View):

    @staticmethod
    def get(request, org_id):
        org = Org.objects.get(id=org_id)
        top_courses = org.course_set.all()[:3]
        top_teachers = org.instructor_set.all()[:3]
        return render(request, "org-detail-homepage.html", {
            "course_org": org,
            "top_courses": top_courses,
            "top_teachers": top_teachers,
            "current_page": "home",
        })


class OrgCourseView(View):

    @staticmethod
    def get(request, org_id):
        org = Org.objects.get(id=org_id)
        all_courses = org.course_set.all()
        all_teachers = org.instructor_set.all()[:3]
        return render(request, "org-detail-course.html", {
            "course_org": org,
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "current_page": "course",
        })


class OrgTeacherView(View):

    @staticmethod
    def get(request, org_id):
        org = Org.objects.get(id=org_id)
        all_teachers = org.instructor_set.all()
        return render(request, "org-detail-teachers.html", {
            "course_org": org,
            "all_teachers": all_teachers,
            "current_page": "teacher",
        })


class OrgDescView(View):

    @staticmethod
    def get(request, org_id):
        org = Org.objects.get(id=org_id)
        return render(request, "org-detail-desc.html", {
            "course_org": org,
            "current_page": "desc",
        })
    # TODO: tests


class AddFavView(View):

    @staticmethod
    def post(request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 'org')
        if request.user.is_authenticated:
            return add_favorite(fav_type, fav_id, request.user)
        else:
            return HttpResponse("{'status': 'failed', 'msg': 'User not login'}")


class TeacherListView(View):

    @staticmethod
    def get(request):
        hot_teachers = Instructor.objects.all().order_by("-hits")
        if request.GET.get("sort", "") == "hot":
            all_teachers = hot_teachers
        else:
            all_teachers = Instructor.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 8, request=request)
        teachers_num = all_teachers.count()
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teachers": hot_teachers[:3],
            "teachers_num": teachers_num,
        })


class TeacherDetailView(View):

    @staticmethod
    def get(request, teacher_id):
        teacher = Instructor.objects.get(id=teacher_id)
        courses = teacher.course_set.all()
        hot_teachers = Instructor.objects.all().order_by("-hits")
        fav_teacher = False
        fav_org = False
        if request.user.is_authenticated and UserFavorite.objects.filter(
                user=request.user, fav_id=teacher.id, fav_type="teacher"):
            fav_teacher = True
        if request.user.is_authenticated and UserFavorite.objects.filter(
                user=request.user, fav_id=teacher.org.id, fav_type="org"):
            fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_courses": courses,
            "sorted_teachers": hot_teachers,
            "has_fav_teacher": fav_teacher,
            "has_fav_org": fav_org,
        })

    # TODO: favorite bug fix


# TODO: add the searching function for instructors, organizations and courses
