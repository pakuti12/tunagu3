from django.db import models
from django.contrib.auth.models import User
# from post.models import Post


# 通知のクラス
class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))

    post = models.ForeignKey("Post_app.Post", on_delete=models.CASCADE, related_name="notification_post", null=True,verbose_name='ポスト')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_from_user",verbose_name='送信者' )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_to_user",verbose_name='受信者' )
    notification_types = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='お知らせ'
    # def __str__(self):
    #     return self.text_preview



