
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View


def index(request):
    return render(request, "index.html", {})


class LoginView(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user:
            login(request=request, user=user)
            return render(request, "index.html", {})
        else:
            return render(request, "login.html", {"msg": "invalid username or password"})

