

from django.urls import path

from organizations.views import (
    OrgListView, UserConsultView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView,
    TeacherListView, TeacherDetailView
)


urlpatterns = [
    path('list/', OrgListView.as_view(), name='org_list'),
    path('consult/', UserConsultView.as_view(), name='add_ask'),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
    path('teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
]
