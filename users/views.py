
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

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
            if user:
                login(request=request, user=user)
                return render(request, "index.html", {})
            else:
                return render(request, "login.html", {"msg": "invalid username or password"})
        return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):

    @staticmethod
    def get(request):
        reg_form = RegisterEmailForm()
        return render(request, "register.html", {"register_form": reg_form})

    @staticmethod
    def post(request):
        reg_form = RegisterEmailForm(request.POST)
        if reg_form.is_valid():
            UserProfile.objects.create(
                username=request.POST['email'],
                email=request.POST['email'],
                password=make_password(request.POST['password']),
                is_active=False,
                is_staff=False,
            )
            unactive_user = UserProfile.objects.get(username=request.POST['email'])
            send_register_verify_mail(unactive_user)
            # send an activation email
            # hit the link on that email lead you to the finish page of registration
            # save this user as a official member in the database
            # TODO: UNIQUE constraint failed on username field
            # TODO: Test for this view and email send util tools
            # TODO: Save literal to a independent file
            # TODO: Only activated user can login
            return render(request, "login.html", {})
        return render(request, "register.html", {"register_form": reg_form})


class ActivateUserView(View):

    @staticmethod
    def get(request, code):
        record = EmailVerify.objects.get(code=code)
        email = record.email
        user = UserProfile.objects.get(email=email)
        if user:
            user.is_active = True
            # TODO: Major bug, repetion username and email address
        return render(request, "index.html", {})
