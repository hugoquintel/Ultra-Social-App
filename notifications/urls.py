from notifications.views import ShowNotifications, DeleteNotification
from django.urls import path

urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),
    path('<noti_id>/delete', DeleteNotification, name='delete-notification'),
]