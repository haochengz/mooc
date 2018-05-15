
from django.urls import path, re_path

from .views import (
    UserInfoView, ImgUploadView, PwdModifyView, MyCoursesView, MyFavOrgView, MyFavCourseView,
    MyFavTeacherView, MyMessageView,
)
import users.views

urlpatterns = [
    path('info/', UserInfoView.as_view(),                                               name='user_info'),
    path('mycourse/', MyCoursesView.as_view(),                                          name="mycourses"),
    path('myfav/org/', MyFavOrgView.as_view(),                                          name="myfav_org"),
    path('myfav/teacher/', MyFavTeacherView.as_view(),                                  name="myfav_teacher"),
    path('myfav/course/', MyFavCourseView.as_view(),                                    name="myfav_course"),
    path('img/upload/', ImgUploadView.as_view(),                                        name="image_upload"),
    path('update/pwd/', PwdModifyView.as_view(),                                        name="update_pwd"),
    path('message/', MyMessageView.as_view(),                                           name="mymessage"),
    path('login/', users.views.LoginView.as_view(),                                     name='login'),
    path('reactive/', users.views.ActivateUserView.as_view(),                           name="resend"),
    path('forget/', users.views.ForgetView.as_view(),                                   name='forget_pwd'),
    path('modify/', users.views.ModifyView.as_view(),                                   name='modify_pwd'),
    path('logout/', users.views.LogoutView.as_view(),                                   name='logout'),
    path('register/', users.views.RegisterView.as_view(),                               name='register'),
    re_path(r'^activate/(?P<code>.*)/$', users.views.ActivateUserView.as_view(),        name="active"),
    re_path(r'^retrieve/(?P<code>.*)/$', users.views.RetrievePasswordView.as_view(),    name="retrieve"),
]
