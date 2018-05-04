
from django.urls import path

from .views import CourseListView, CourseDetailView, CourseInfoView

urlpatterns = [
    path('list/', CourseListView.as_view(), name="course_list"),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name="course_detail"),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name="course_info"),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name="course_comments"),
]