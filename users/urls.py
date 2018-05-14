
from django.urls import path

from .views import UserInfoView, ImgUploadView, PwdModifyView, MyCoursesView, MyFavOrgView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('myfav/org/', MyCoursesView.as_view(), name="mycourses"),
    path('mycours/', MyFavOrgView.as_view(), name="myfav_org"),
    path('img/upload/', ImgUploadView.as_view(), name="image_upload"),
    path('update/pwd/', PwdModifyView.as_view(), name="update_pwd"),
    path('mycours/', MyFavOrgView.as_view(), name="myfav_teacher"),
    path('mycours/', MyFavOrgView.as_view(), name="myfav_course"),
]
