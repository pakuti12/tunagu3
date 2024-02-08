from django.contrib import admin

# Register your models here.
from comment_app.models import Comment
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','post','body','date']
admin.site.register(Comment,CommentAdmin)
