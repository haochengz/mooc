
from django.urls import path

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddCommentView, VideoPlayView

urlpatterns = [
    path('list/', CourseListView.as_view(), name="course_list"),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name="course_detail"),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name="course_info"),
    path('comment/<int:course_id>/', CommentView.as_view(), name="course_comments"),
    path('add/', AddCommentView.as_view(), name="add_comment"),
    path('video/<int:video_id>/', VideoPlayView.as_view(), name="video_play"),
]