from django.contrib import admin
from direct_app.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display=['user','sender','reciepient','body','date']
admin.site.register(Message,MessageAdmin)
