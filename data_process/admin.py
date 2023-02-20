from django.contrib import admin
from . import models

# Register your models here.

#register = admin.site.register(models.UserInfo)


@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'password']
    list_display_links = ['name']

