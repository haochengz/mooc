
from django.urls import path

from .views import UserInfoView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('mycourse/', UserInfoView.as_view(), name="mycourses"),  # Dummy
    path('mycours/', UserInfoView.as_view(), name="myfav_org"),  # Dummy
    path('mycour/', UserInfoView.as_view(), name="image_upload"),  # Dummy
]
