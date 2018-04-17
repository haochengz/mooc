from django.contrib import admin

from .models import Course, Chapter, Section, Resource


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "name", "degree", "duration_mins", "enrolled_nums", "favorite_nums", "hits", "add_time"
    ]
    search_fields = [
        "name", "degree", "duration_mins", "enrolled_nums", "favorite_nums", "hits",
        "desc", "detail",
    ]
    list_filter = [
        "name", "degree", "duration_mins", "enrolled_nums", "favorite_nums", "hits", "add_time"
    ]


class ChapterAdmin(admin.ModelAdmin):
    list_display = [
        "course", "name", "add_time",
    ]
    search_fields = [
        "course", "name",
    ]
    list_filter = [
        "course", "name", "add_time",
    ]


class SectionAdmin(admin.ModelAdmin):
    list_display = [
        "chapter", "name", "add_time",
    ]
    search_fields = [
        "chapter", "name",
    ]
    list_filter = [
        "chapter", "name", "add_time",
    ]


class ResourceAdmin(admin.ModelAdmin):
    list_display = [
        "course", "name", "add_time", "path",
    ]
    search_fields = [
        "course", "name", "add_time",
    ]
    list_filter = [
        "course", "name", "add_time",
    ]


admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Resource, ResourceAdmin)
