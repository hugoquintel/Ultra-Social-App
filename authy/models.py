from django.db import models
from django.contrib.auth.models import User
from post.models import Post

from django.db.models.signals import post_save

# Create your models here.
def user_profile_path(instance, filename):
    # This file will be upload to MEDIA_ROOT /user(id)/filename
    return f'user_{instance.user.id}/profile.jpg'

def user_background_path(instance, filename):
    # This file will be upload to MEDIA_ROOT /user(id)/filename
    return f'user_{instance.user.id}/background.jpg'

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	picture = models.ImageField(upload_to=user_profile_path, blank=True, null=True, verbose_name='Picture')
	backgroundimage = models.ImageField(upload_to=user_background_path, blank=True, null=True, verbose_name='Background')

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)