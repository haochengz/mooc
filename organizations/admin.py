from django.contrib import admin

from .models import Location, Org, Instructor


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name", "desc", "add_time",
    ]
    search_fields = [
        "name", "desc",
    ]
    list_filter = [
        "name", "desc", "add_time",
    ]


class OrgAdmin(admin.ModelAdmin):
    list_display = [
        "name", "hits", "favorite_nums", "located",
    ]
    search_fields = [
        "name", "hits", "favorite_nums", "located", "desc", "address",
    ]
    list_filter = [
        "name", "hits", "favorite_nums", "located",
    ]


class InstructorAdmin(admin.ModelAdmin):
    list_display = [
        "name", "hits", "favorite_nums", "org", "employed", "position", "service_len",
    ]
    search_fields = [
        "name", "hits", "favorite_nums", "org", "employed", "position", "service_len", "characteristics",
    ]
    list_filter = [
        "name", "hits", "favorite_nums", "org", "employed", "position", "service_len", "characteristics", "add_time",
    ]


admin.site.register(Location, LocationAdmin)
admin.site.register(Org, OrgAdmin)
admin.site.register(Instructor, InstructorAdmin)
