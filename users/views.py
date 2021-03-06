
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, PageNotAnInteger

from users.forms import (
    LoginForm, RegisterEmailForm, ForgetForm, PasswordResetForm, ImgUploadForm, UserCenterPwResetForm,
    UserInfoForm,
)
from users.models import UserProfile, EmailVerify, Banner
from organizations.models import Org, Instructor
from courses.models import Course
from operations.models import UserCourse, UserFavorite, UserMessage
from apps.utils.email import send_register_verify_mail, send_retrieve_password_mail
from apps.utils.tools import LoginRequiredMixin


class IndexView(View):

    @staticmethod
    def get(request):
        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_ad=False).order_by("-hits")[:6]
        advertise = Course.objects.filter(is_ad=True)
        courses_orgs = Org.objects.all().order_by("hits")[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": advertise,
            "course_orgs": courses_orgs,
        })


class LoginView(View):

    @staticmethod
    def get(request):
        return render(request, "login.html", {})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request=request, user=user)
                from django.urls import reverse
                return HttpResponseRedirect(reverse("index"))
            elif not user:
                return render(request, "login.html", {"msg": "invalid username or password"})
            else:
                return render(request, "login.html", {"msg": "user %s is not activated" % user.username})
        return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):

    @staticmethod
    def get(request):
        reg_form = RegisterEmailForm()
        return render(request, "register.html", {"register_form": reg_form})

    @staticmethod
    def post(request):
        reg_form = RegisterEmailForm(request.POST)
        repeat = UserProfile.objects.filter(Q(username=request.POST['email']) | Q(email=request.POST['email']))
        if reg_form.is_valid() and len(repeat) == 0:
            unactive_user = UserProfile.objects.create(
                username=request.POST['email'],
                email=request.POST['email'],
                password=make_password(request.POST['password']),
                is_active=False,
                is_staff=False,
            )
            send_register_verify_mail(unactive_user)
            return render(request, "login.html", {"msg": "Check your email to activate"})
        elif len(repeat) > 0:
            return render(request, "register.html", {"register_form": reg_form, "msg": "email already exists"})
        return render(request, "register.html", {"register_form": reg_form})


class ActivateUserView(View):

    @staticmethod
    def get(request, code):
        record = EmailVerify.objects.filter(code=code)
        if len(record) != 1:
            return render(request, "verify.html", {"msg": "cannot activate user, active code is wrong"})
        elif (timezone.now() - record[0].send_time).total_seconds() > 1800:
            EmailVerify.objects.filter(code=code).delete()
            return render(request, "verify.html", {"msg": "the validation code is out of date"})
        email = record[0].email
        user = UserProfile.objects.get(email=email)
        if user:
            EmailVerify.objects.filter(code=code).delete()
            user.is_active = True
            user.save()
        return render(request, "login.html", {"msg": "verify success, please login"})

    @staticmethod
    def post(request):
        email = request.POST['email']
        users = UserProfile.objects.filter(email=email)
        if users.count() == 0:
            return render(request, "verify.html", {"msg": "email address didn't found, please register first"})
        elif users[0].is_active:
            return render(request, "verify.html", {"msg": "email address already been activated"})
        else:
            record = EmailVerify.objects.filter(email=email)
            last_send_time = sorted(record, key=lambda x: x.send_time)
            period = (timezone.now() - last_send_time[-1].send_time).total_seconds()
            if period < 900:
                return render(request, "verify.html",
                              {"msg": "same email address only re-send a validation code every 15 minutes"})
            send_register_verify_mail(users[0])
            return render(request, "login.html", {})


class ForgetView(View):

    @staticmethod
    def get(request):
        form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": form})

    @staticmethod
    def post(request):
        form = ForgetForm(request.POST)
        if form.is_valid():
            user = UserProfile.objects.filter(email=request.POST['email'])
            if len(user) == 0:
                return render(request, "forgetpwd.html", {"msg": "Wrong email address"})
            send_retrieve_password_mail(user[0])
            return render(request, "index.html", {})
        return render(request, "forgetpwd.html", {"forget_form": form})

    # TODO: when send the retrieve password email, should give user a hint that email was send away
    # TODO: What if multiple validation code stored in db that relative to one user


class RetrievePasswordView(View):

    @staticmethod
    def get(request, code):
        form = PasswordResetForm()
        records = EmailVerify.objects.filter(code=code, verify_type="forget")
        if len(records) == 0:
            return render(request, "register.html", {"msg": "Wrong validation code"})
        elif (timezone.now() - records[0].send_time).total_seconds() > 1800:
            records[0].delete()
            return render(request, "register.html", {"msg": "validation code out of date"})
        email = records[0].email
        records[0].delete()
        return render(request, "password_reset.html", {"email": email, "reset_form": form})

# TODO: Modify email address View and function un-implement


class ModifyView(View):

    @staticmethod
    def post(request):
        form = PasswordResetForm(request.POST)
        email = request.POST['email']
        if form.is_valid():
            if request.POST['pwd1'] != request.POST['pwd2']:
                return render(request, "password_reset.html", {
                    "email": email,
                    "reset_form": form,
                    "msg": "password were different between two enters"
                })
            user = UserProfile.objects.get(email=email)
            user.password = make_password(request.POST['pwd2'])
            user.save()
            return render(request, "login.html", {"msg": "reset success, please login."})
        else:
            return render(request, "password_reset.html", {"email": email, "reset_form": form})


class UserInfoView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        return render(request, "usercenter-info.html", {
        })

    @staticmethod
    def post(request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status': 'success'}", content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class ImgUploadView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        image_form = ImgUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse("{'status': 'success'}", content_type="application/json")
        else:
            return HttpResponse("{'status': 'fail'}", content_type="application/json")


class PwdModifyView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        pwd_reset_form = UserCenterPwResetForm(request.POST)
        if pwd_reset_form.is_valid():
            pwd1 = request.POST['password1']
            pwd2 = request.POST['password2']
            if pwd1 != pwd2:
                return HttpResponse("{'status': 'fail', 'msg': 'Wrong input'}", content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse("{'status': 'success', 'msg': 'success, please re-login'}",
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps(pwd_reset_form.errors), content_type="application/json")


class MyCoursesView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type="org")
        orgs = [Org.objects.get(id=org.fav_id) for org in fav_orgs]
        return render(request, "usercenter-fav-org.html", {
            "org_list": orgs,
        })


class MyFavTeacherView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type="teacher")
        teachers = [Instructor.objects.get(id=teacher.fav_id) for teacher in fav_teachers]
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teachers,
        })


class MyFavCourseView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type="course")
        courses = [Course.objects.get(id=course.fav_id) for course in fav_courses]
        return render(request, "usercenter-fav-course.html", {
            "course_list": courses,
        })


class MyMessageView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        user_messages = UserMessage.objects.filter(user=request.user).order_by("-add_time")
        paginator = Paginator(user_messages, 8, request=request)
        messages = paginator.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


class LogoutView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"))


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def server_internal_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response


def test_404_render(request):
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def test_500_render(request):
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response
