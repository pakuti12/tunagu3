from django.contrib import admin
from Post_app.models import *
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['caption','user','category',]
class FollowAdmin(admin.ModelAdmin):
    list_display=['follower','following']
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','category_image']
class StreamAdmin(admin.ModelAdmin):
    list_display=['user','following','post','date']
class LikeAdmin(admin.ModelAdmin):
    list_display=['user','post']





admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Follow,FollowAdmin)
admin.site.register(Stream,StreamAdmin)
admin.site.register(Likes,LikeAdmin)

