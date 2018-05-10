
from django.urls import path

from .views import UserInfoView, ImgUploadView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('mycourse/', UserInfoView.as_view(), name="mycourses"),  # Dummy
    path('mycours/', UserInfoView.as_view(), name="myfav_org"),  # Dummy
    path('img/upload/', ImgUploadView.as_view(), name="image_upload"),  # Dummy
]
