from django.db import models
from django.contrib.auth.models import User
import shortuuid
from shortuuid.django_fields import ShortUUIDField


from django.db.models.signals import post_save

import os
from django.conf import settings
from django.utils import timezone

# Create your models here.
#def user_directory_path(instance, filename):

def user_directory_path(instance, filename):
     # this function will upload to MEDIA_ROOT /user{id}/filename
	profile_pic_name = 'user{0}/profile_{1}.jpg'.format(instance.user.id, filename)
	full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

	if os.path.exists(full_path):
		os.remove(full_path)

	return profile_pic_name

def default_profile_picture():
    default_profile_pic_name = 'media/profile_picture/default.png'
    full_path = os.path.join(settings.MEDIA_ROOT, default_profile_pic_name)
    print(full_path)
    
    if os.path.exists(full_path):
        return full_path

class Profile(models.Model):
    # During Sign Up
    profile_id = ShortUUIDField(primary_key=True, length=11, max_length=11, editable=False)
    user_obj = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    birth_date = models.DateField(max_length=8, null=True, blank=True)
    
    # Can edit after created account
    bio = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    picture = models.ImageField(upload_to=user_directory_path, default='media/profile_picture/default.png', blank=True, null=True)
    # following = models.ManyToManyField(User, blank=True, related_name='user_follower')

    def __str__(self):
        return self.user_obj.username

    # def get_follower(self):
    #     return self.follower

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_obj=instance)

post_save.connect(create_user_profile, sender=User)
