from django.shortcuts import render
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "index.html", {})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user:
            login(request=request, user=user)
            return render(request, "index.html", {})
    return render(request, "login.html", {})
