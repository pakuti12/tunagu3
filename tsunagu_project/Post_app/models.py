from django.db import models
from shortuuid.django_fields import ShortUUIDField
# Create your models here.
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete
from notification_app.models import *

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# カテゴリを作る時のモデル（管理者画面でのみ閲覧可能）
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="cat", alphabet="abcdefgh12345",verbose_name='カテゴリーのid')
    title = models.CharField(max_length=100, default="Food",verbose_name='カテゴリー名')
    image = models.ImageField(upload_to="category", default="category.jpg",verbose_name='カテゴリーの写真')
    class Meta:
        verbose_name_plural = "カテゴリー"

    def category_image(self):
        return mark_safe('<img src="%s" width="150" height="50" />' % (self.image.url))



    def __str__(self):
        return self.title
    
#タグ付けする時のモデル
class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='タグ')
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

# 投稿する時に使うモデル
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name='ポストid')
    category = models.ForeignKey( Category, on_delete=models.SET_NULL, null=True, related_name="category",verbose_name='カテゴリー')
    picture = models.ImageField( upload_to=user_directory_path, default="product.jpg",verbose_name='ポストの写真')
    caption = models.CharField(max_length=100, default="Fresh Pear",verbose_name='ポスト名')
    tags=models.ManyToManyField(Tag,related_name='tags',verbose_name='タグ')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='ユーザ')
    posted = models.DateField(auto_now_add=True)

    likes = models.IntegerField(default=0)
    status = models.BooleanField(default=True,verbose_name='ステータス')
    # section=models.ForeignKey(Section,on_delete=models.SET_NULL,null=True,verbose_name='セクション')
    class Meta:
        verbose_name_plural='ポスト'
    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])



    

# フォローするときのモデル
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name_plural='フォロー'
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification(sender=sender, user=following, notification_types=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification.objects.filter(sender=sender, user=following, notification_types=3)
        notify.delete()

# 投稿を入れる
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='ユーザ')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,verbose_name='ポスト')
    date = models.DateTimeField()


    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()

# いいね
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_types=1)
        notify.delete()

post_save.connect(Stream.add_post, sender=Post)
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)