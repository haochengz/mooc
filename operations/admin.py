from django.contrib import admin

from .models import UserFavorite, UserCourse, UserMessage, UserConsult, CourseComment


class UserFacoriteAdmin(admin.ModelAdmin):
    list_display = [
        "user", "fav_type", "add_time",
    ]
    search_fields = [
        "user", "fav_type"
    ]
    list_filter = [
        "user", "fav_type", "add_time",
    ]


class UserCourseAdmin(admin.ModelAdmin):
    list_display = [
        "user", "course", "add_time",
    ]
    search_fields = [
        "user", "course"
    ]
    list_filter = [
        "user", "course", "add_time",
    ]


class UserMessageAdmin(admin.ModelAdmin):
    list_display = [
        "user", "is_read", "message", "add_time",
    ]
    search_fields = [
        "user", "message",
    ]
    list_filter = [
        "user", "is_read", "message", "add_time",
    ]


class UserConsultAdmin(admin.ModelAdmin):
    list_display = [
        "name", "course_name", "mobile", "add_time",
    ]
    search_fields = [
        "name", "course_name", "mobile",
    ]
    list_filter = [
        "name", "course_name", "mobile", "add_time",
    ]


class CourseCommentAdmin(admin.ModelAdmin):
    list_display = [
        "user", "course", "comment", "add_time",
    ]
    search_fields = [
        "user", "course", "comment",
    ]
    list_filter = [
        "user", "course", "comment", "add_time",
    ]


admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(UserConsult, UserConsultAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserFavorite, UserFacoriteAdmin)
