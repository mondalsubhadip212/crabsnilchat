"""
ASGI config for Chat_Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django


from channels.routing import ProtocolTypeRouter,URLRouter
from channels.routing import get_asgi_application
from channels.auth import AuthMiddlewareStack
import crabsnil_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_project.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket" :
     AuthMiddlewareStack(
        URLRouter(
            crabsnil_chat.routing.websocket_urlpatterns
        )
    )
})
