
from django.urls import path

from .views import (
    UserInfoView, ImgUploadView, PwdModifyView, MyCoursesView, MyFavOrgView, MyFavCourseView,
    MyFavTeacherView, MyMessageView,
)

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('mycourse/', MyCoursesView.as_view(), name="mycourses"),
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),
    path('img/upload/', ImgUploadView.as_view(), name="image_upload"),
    path('update/pwd/', PwdModifyView.as_view(), name="update_pwd"),
    path('message/', MyMessageView.as_view(), name="mymessage"),
]
