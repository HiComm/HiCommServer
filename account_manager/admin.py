from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = ((None, {"fields" : ("company_id",)}),)
    list_display = ["username", "email", "company_id"]

# add CustomUser to admin view
admin.site.register(CustomUser, CustomUserAdmin)