

from django.urls import path, re_path, include

from organizations.views import OrgListView


urlpatterns = [
    path('', OrgListView.as_view(), name='org_list'),
    path('consult/', OrgListView.as_view(), name='add_ask'),
]
