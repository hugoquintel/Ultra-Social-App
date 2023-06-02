"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authy.views import UserProfile, follow, Direct

app_name = "main"
urlpatterns = [
    # admin url
    path('admin/', admin.site.urls),

    # own
    path('', Direct),
    path('post/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('stories/', include('stories.urls')),
    path('direct/', include('direct.urls')),
    path('notifications/', include('notifications.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', UserProfile, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
