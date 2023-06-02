from django.db import models
from post.models import Post
from notifications.models import Notification

from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save, post_delete


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    

    def user_comment_post(sender, instance, *args, **kwargs):
        comment=instance
        post=comment.post
        text_preview = comment.body
        if len(text_preview) > 90:
            text_preview = comment.body[:90] + '...'
        else:
            text_preview = comment.body
        sender=comment.user

        if sender == post.user:
            pass
        else:
            notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
            notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        comment=instance
        post=comment.post
        sender=comment.user

        notify = Notification.objects.filter(post=post, sender=sender, user=post.user, notification_type=2)
        notify.delete()

# Comment signals
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)