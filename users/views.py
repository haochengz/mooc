from django.shortcuts import render


def index(request):
    pass


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        username, password
    return render(request, "login.html", {})
