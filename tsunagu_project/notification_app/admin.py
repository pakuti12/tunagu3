from django.contrib import admin
from notification_app.models import *
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display=['user','sender','notification_types','post','date']
admin.site.register(Notification,NotificationAdmin)
