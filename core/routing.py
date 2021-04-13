from core import consumers

from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws$', consumers.SyncChatConsumer.as_asgi()),
]
# websocket_urlpatterns = [

#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]