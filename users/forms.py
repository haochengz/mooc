
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=32, min_length=4)
    password = forms.CharField(required=True, max_length=16, min_length=8)
