
from django.urls import path

from .views import CourseListView

urlpatterns = [
    # path('course_detail/<int:org_id>/', OrgHomeView.as_view(), name='course_detail'),       # FIXME:
    path('list/', CourseListView.as_view(), name="course_list"),
]