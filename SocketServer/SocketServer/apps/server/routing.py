from django.conf.urls import url
from .consumers import AsyncChatConsumer



websocket_urls = [
    url(r'^ws/chat/(?P<room_name>\w+)/$', AsyncChatConsumer.as_asgi()),
]