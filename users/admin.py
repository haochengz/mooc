from django.contrib import admin

from .models import UserProfile, EmailVerify, Banner


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username", "nick_name", "gender", "mobile", "email",
    ]
    search_fields = [
        "username", "nick_name", "mobile", "first_name", "last_name", "address", "gender", "email"
    ]
    list_filter = [
        "username", "nick_name", "mobile", "first_name", "last_name", "address", "gender",
        "is_staff", "is_active", "email", "date_joined",
    ]


class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = [
        "email", "code", "verify_type", "send_time",
    ]
    list_filter = [
        "email", "code", "verify_type", "send_time",
    ]
    search_fields = [
        "email", "code", "verify_type",
    ]


class BannerAdmin(admin.ModelAdmin):
    list_display = [
        "title", "url", "index", "add_time",
    ]
    search_fields = [
        "title", "url", "index",
    ]
    list_filter = [
        "title", "url", "index", "add_time",
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerify, EmailVerifyAdmin)
admin.site.register(Banner, BannerAdmin)

