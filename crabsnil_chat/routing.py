from django.urls import path

from .consumer import ChatConsumer

websocket_urlpatterns = [
    path('chat/<str:id>', ChatConsumer.as_asgi()),
]
