
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django_private_chat2 import urls as django_private_chat2_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('user_feeds/', include('user_feeds.urls')),
    path('discussion_forum/', include('Forum.urls')),
    path('chat/', include('chat.urls')),
    path('', include(django_private_chat2_urls)),
    path('', include('homepage.urls')),
 
 
   
  
]

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

