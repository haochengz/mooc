
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=32, min_length=4)
    password = forms.CharField(required=True, max_length=16, min_length=8)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=32, min_length=4)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=16, min_length=8)
    captcha = CaptchaField()

