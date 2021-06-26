"""
ASGI config for Chat_Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.conf.urls import url
from django.core.asgi import get_asgi_application

# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "message_project.settings")
django_asgi_app = get_asgi_application()


# 
from channels.routing import ProtocolTypeRouter,URLRouter, get_asgi_application
from channels.auth import AuthMiddlewareStack



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket" :
     AuthMiddlewareStack(
        URLRouter(
            crabsnil_chat.routing.websocket_urlpatterns
        )
    )
})
