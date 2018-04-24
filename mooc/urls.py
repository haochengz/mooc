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

import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.views.index, name='index'),
    path('login/', users.views.LoginView.as_view(), name='login'),
    path('reactive/', users.views.ActivateUserView.as_view(), name="resend"),
    path('forget/', users.views.ForgetView.as_view(), name='forget_pwd'),
    path('modify/', users.views.ModifyView.as_view(), name='modify_pwd'),
    path('info/', TemplateView.as_view(template_name='index.html'), name='user_info'),
    path('logout/', TemplateView.as_view(template_name='index.html'), name='logout'),
    path('message/', TemplateView.as_view(template_name='index.html'), name='mymessage'),
    path('register/', users.views.RegisterView.as_view(), name='register'),
    path('courses/', TemplateView.as_view(template_name='index.html'), name='course_list'),
    path('teachers/', TemplateView.as_view(template_name='index.html'), name='teacher_list'),
    path('orgs/', TemplateView.as_view(template_name='index.html'), name='org_list'),
    path('orghome/', TemplateView.as_view(template_name='index.html'), name='org_home'),
    path('coursedetail/', TemplateView.as_view(template_name='index.html'), name='course_detail'),
    path('captcha/', include('captcha.urls')),
    re_path(r'^activate/(?P<code>.*)/$', users.views.ActivateUserView.as_view(), name="active"),
    re_path(r'^retrieve/(?P<code>.*)/$', users.views.RetrievePasswordView.as_view(), name="retrieve"),
]
