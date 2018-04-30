

from django.urls import path, re_path

from organizations.views import OrgListView, UserConsultView


urlpatterns = [
    path('', OrgListView.as_view(), name='org_list'),
    path('consult/', UserConsultView.as_view(), name='add_ask'),
    re_path(r'^home/(?P<org_id>\d+)\$')
]
