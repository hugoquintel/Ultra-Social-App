from celery import shared_task
from stories.models import Story, StoryStream

from datetime import datetime, timedelta

#Task to check the stories date
@shared_task
def CheckStoriesDate():
	exp_date = datetime.now() - timedelta(minutes=1)
	old_stories = Story.objects.filter(posted__lt=exp_date)
	print(old_stories)
	old_stories.update(expired=True)
	print('Story updated')

#Task to Delete the stories marked as expired by the CheckStoriesDate task
@shared_task
def DeleteExpired():
	Story.objects.filter(expired=True).delete()
	StoryStream.objects.filter(story=None).delete()
	print('Story deleted')