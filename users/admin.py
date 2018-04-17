from django.contrib import admin

from .models import UserProfile, EmailVerify, Banner


class UserProfileAdmin(admin.ModelAdmin):
    pass


class EmailVerifyAdmin(admin.ModelAdmin):
    pass


class BannerAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerify, EmailVerifyAdmin)
admin.site.register(Banner, BannerAdmin)

