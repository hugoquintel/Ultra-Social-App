from django.contrib import admin

# Register your models here.
from stories.models import Story, StoryStream

admin.site.register(Story)
admin.site.register(StoryStream)