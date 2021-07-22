from django.contrib import admin

from .models import CustomUser as User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


admin.site.register(User, UserAdmin)
