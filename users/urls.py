
from django.urls import path

from .views import UserInfoView, ImgUploadView, PwdModifyView, MyCoursesView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('mycourse/', MyCoursesView.as_view(), name="mycourses"),
    path('mycours/', UserInfoView.as_view(), name="myfav_org"),  # Dummy
    path('img/upload/', ImgUploadView.as_view(), name="image_upload"),
    path('update/pwd/', PwdModifyView.as_view(), name="update_pwd"),
]
