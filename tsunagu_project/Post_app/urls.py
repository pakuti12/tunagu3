from django.urls import path,include
from Post_app import views
urlpatterns = [
path('',views.home,name='home'),
path('newpost', views.NewPost, name='newpost'),
path('<uuid:post_id>', views.PostDetail, name='post-details'),
path('<uuid:post_id>/like', views.like, name='like'),
    path('<uuid:post_id>/favourite', views.favourite, name='favourite'),

     path('category/',views.category_list,name="category"),
 path('category_Post_list/<cid>/',views.category_Post_list,name="category-post-list"),




]