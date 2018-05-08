"""mooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

import users.views
from mooc.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.views.index, name='index'),
    path('orgs/', include('organizations.urls')),
    path('course/', include('courses.urls')),
    path('login/', users.views.LoginView.as_view(), name='login'),
    path('reactive/', users.views.ActivateUserView.as_view(), name="resend"),
    path('forget/', users.views.ForgetView.as_view(), name='forget_pwd'),
    path('modify/', users.views.ModifyView.as_view(), name='modify_pwd'),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('info/', TemplateView.as_view(template_name='index.html'), name='user_info'),
    path('logout/', TemplateView.as_view(template_name='index.html'), name='logout'),
    path('message/', TemplateView.as_view(template_name='index.html'), name='mymessage'),
    path('register/', users.views.RegisterView.as_view(), name='register'),
    re_path(r'^activate/(?P<code>.*)/$', users.views.ActivateUserView.as_view(), name="active"),
    re_path(r'^retrieve/(?P<code>.*)/$', users.views.RetrievePasswordView.as_view(), name="retrieve"),
    path('captcha/', include('captcha.urls')),
]
