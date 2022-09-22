from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
import uuid

from accounts . models import Profile

from mptt.models import MPTTModel, TreeForeignKey

#from model_utils.managers import InheritanceManager

#Multi step submission
#https://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django
# Create your models here.

def user_directory_path(instance, filename):
    return 'user{0}/{1}'.format(instance.user.id, filename)

class MediaStream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Post(MediaStream):
    quackid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_body = models.CharField(max_length=256)
    # following = models.ManyToManyField(User, blank=True, null=True, related_name='following_person') # Who does user follow.
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    shares = models.ManyToManyField(User, blank=True, related_name='post_shares')
    bookmark = models.ManyToManyField(User, blank=True, related_name='post_bookmark')
    updated = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.post_body

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.quackid)])

    def get_comments(self):
        return self.post_commented.filter(parent=None).filter(active=True)

    def get_share_count(self):
        return self.post_shared.count()

class Comment(MediaStream, MPTTModel):
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_commented', null=True, blank=True)
    commented_body = models.TextField()
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    shares = models.ManyToManyField(User, blank=True, related_name='comment_shares')
    bookmark = models.ManyToManyField(User, blank=True, related_name='comment_bookmark')

    def __str__(self):
        return str(self.pk) + " " + self.commented_body

    def get_children(self):
        return Comment.objects.filter(parent=self)

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Share'), (3, 'PostComment'), (4, 'CommentReply'), (5, 'Follow'))

    notification_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_notification', null=True, blank=True)
    notification_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'comment_notification', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'noti_from_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'noti_to_user')
    notification_types = models.IntegerField(choices = NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=30, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

class Like(MediaStream):
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_liked', null=True, blank=True)
    liked_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'comment_liked', null=True, blank=True)
   
    def __str__(self):
        if self.liked_post is None:
            liked_obj = self.liked_comment
        else:
            liked_obj = self.liked_post

        return  '%s - %s - %s' % (str(self.pk), liked_obj, self.user)
        # return  '%s - %s' % (liked_obj, self.user)

class Share(MediaStream):
    shared_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_shared', null=True, blank=True)
    shared_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'comment_shared', null=True, blank=True)
    commented_body = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.shared_post is None:
            liked_obj = self.shared_comment
        else:
            liked_obj = self.shared_post

        return  '%s - %s - %s' % (str(self.pk), liked_obj, self.user)

class Bookmark(MediaStream):
    bookmark_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_bookmark', null=True, blank=True)
    bookmark_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'comment_bookmark', null=True, blank=True)
