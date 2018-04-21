
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import IntegrityError

from users.forms import LoginForm, RegisterEmailForm
from users.models import UserProfile, EmailVerify
from apps.utils.email import send_register_verify_mail


def index(request):
    return render(request, "index.html", {})


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
                return render(request, "index.html", {})
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
            UserProfile.objects.create(
                username=request.POST['email'],
                email=request.POST['email'],
                password=make_password(request.POST['password']),
                is_active=False,
                is_staff=False,
            )
            unactive_user = UserProfile.objects.get(username=request.POST['email'])
            send_register_verify_mail(unactive_user)
            return render(request, "login.html", {})
        elif len(repeat) > 0:
            return render(request, "register.html", {"msg": "email already exists"})
        return render(request, "register.html", {"register_form": reg_form})


class ActivateUserView(View):

    @staticmethod
    def get(request, code):
        record = EmailVerify.objects.filter(code=code)
        if len(record) != 1:
            return render(request, "register.html", {"msg": "cannot activate user, active code is wrong"})
        email = record[0].email
        user = UserProfile.objects.get(email=email)
        if user:
            user.is_active = True
            user.save()
        return render(request, "index.html", {})

    # TODO: very unlikely but still had a tiny chance that might been produced a same verify code
    # TODO: setup a page to re-send verify code email
    # TODO: re-send verify code should only every 15 minutes interval
    # TODO: verify code may out of date
    # TODO: warn the user period of validity in the verify mail
    # TODO: once code has been verified, delete it from db
