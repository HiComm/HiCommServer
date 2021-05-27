from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notification

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = ((None, {"fields" : ("company_id",)}),)
    list_display = ["username", "email", "company_id"]

class NotificationAdmin(Notification):
    model = Notification
    fieldsets = ((None, {"fields" : ("body", )}),)
    list_display = ["body", "date_published", "post_to"]

# add CustomUser to admin view
admin.site.register([CustomUser, Notification])