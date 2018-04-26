
from django.views.generic import View
from django.shortcuts import render

from .models import Org, Location


class OrgListView(View):

    @staticmethod
    def get(request):
        all_orgs = Org.objects.all()
        all_cities = Location.objects.all()
        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
            "all_cities": all_cities,
            "org_nums": all_orgs.count(),
        })
