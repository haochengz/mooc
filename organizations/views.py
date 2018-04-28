
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
        sort_by = request.GET.get('sort', '')

        all_cities = Location.objects.all()
        all_orgs = Org.objects.all()
        top_orgs = all_orgs.order_by("-hits")[:3]

        if city_id:
            all_orgs = all_orgs.filter(located_id=city_id)
        if category:
            all_orgs = all_orgs.filter(category=category)
        if sort_by:
            if sort_by == "students":
                all_orgs = all_orgs.order_by("-enrolled_nums")
            elif sort_by == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        paginator = Paginator(all_orgs, 8, request=request)
        orgs = paginator.page(page)
        return render(request, "org-list.html", {
            "orgs": orgs,
            "all_cities": all_cities,
            "org_nums": all_orgs.count(),
            "city_id": city_id,
            "category": category,
            "top_orgs": top_orgs,
            "sort": sort_by,
        })

    # TODO: test pagination
    # TODO: test sift organizations
    # TODO: test top 3 orgs shows at right side of the page
    # TODO: test sort by enrolled students number of open course number
