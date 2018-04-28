

from django.urls import path, re_path, include

from organizations.views import OrgListView, UserConsultView


urlpatterns = [
    path('', OrgListView.as_view(), name='org_list'),
    path('consult/', UserConsultView.as_view(), name='add_ask'),
]