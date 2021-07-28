from django.contrib import admin

from .models import CustomUser, FollowModel


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


@admin.register(FollowModel)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.register(CustomUser, UserAdmin)
