
from django.views.generic import View
from django.shortcuts import render

# Create your views here.


class CourseListView(View):

    @staticmethod
    def get(request):
        return render(request, "course-list.html", {})
