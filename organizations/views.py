
from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

from .models import Org, Location


class OrgListView(View):

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        all_cities = Location.objects.all()
        all_orgs = Org.objects.all()

        if city_id:
            all_orgs = all_orgs.filter(located_id=city_id)
        if category:
            all_orgs = all_orgs.filter(category=category)

        paginator = Paginator(all_orgs, 8, request=request)
        orgs = paginator.page(page)
        return render(request, "org-list.html", {
            "orgs": orgs,
            "all_cities": all_cities,
            "org_nums": all_orgs.count(),
            "city_id": city_id,
            "category": category,
        })

    # TODO: test pagination
    # TODO:
