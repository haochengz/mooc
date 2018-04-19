
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.forms import LoginForm, RegisterEmailForm
from users.models import UserProfile
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
        reg_form.email = ""
        reg_form.password = ""
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
            unactivate_user = UserProfile.objects.get(username=request.POST['email'])
            send_register_verify_mail(unactivate_user)
            # send an activation email
            # hit the link on that email lead you to the finish page of registration
            # save this user as a official member in the database
        return render(request, "register.html", {"register_form": reg_form})
