
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone

from users.forms import LoginForm, RegisterEmailForm, ForgetForm, PasswordResetForm, ImgUploadForm
from users.models import UserProfile, EmailVerify
from apps.utils.email import send_register_verify_mail, send_retrieve_password_mail
from apps.utils.tools import LoginRequiredMixin


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


class ImgUploadView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        image_form = ImgUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
