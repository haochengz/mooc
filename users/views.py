
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View

from users.forms import LoginForm, RegisterForm


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
        reg_form = RegisterForm()
        return render(request, "register.html", {"register_form": reg_form})

    @staticmethod
    def post(request):
        pass
