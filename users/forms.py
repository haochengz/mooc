
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=32, min_length=4)
    password = forms.CharField(required=True, max_length=16, min_length=8)


class RegisterEmailForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=16, min_length=8)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class PasswordResetForm(forms.Form):
    pwd1 = forms.CharField(required=True, max_length=16, min_length=8)
    pwd2 = forms.CharField(required=True, max_length=16, min_length=8)


class ImgUploadForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image', ]
