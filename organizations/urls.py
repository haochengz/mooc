

from django.urls import path

from organizations.views import (
    OrgListView, UserConsultView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
)


urlpatterns = [
    path('', OrgListView.as_view(), name='org_list'),
    path('consult/', UserConsultView.as_view(), name='add_ask'),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),

    path('add_fav/', OrgListView.as_view(), name='add_fav'),                                # FIXME:
    path('course_detail/<int:org_id>/', OrgHomeView.as_view(), name='course_detail'),       # FIXME:



]
