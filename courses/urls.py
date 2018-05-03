
from django.urls import path

from .views import CourseListView, CourseDetailView

urlpatterns = [
    # path('course_detail/<int:org_id>/', OrgHomeView.as_view(), name='course_detail'),       # FIXME:
    path('list/', CourseListView.as_view(), name="course_list"),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name="course_detail"),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name="course_info"),
]