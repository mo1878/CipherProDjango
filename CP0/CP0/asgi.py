"""
ASGI config for CP0 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from CP0_frontend import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CP0.settings')

websocket_urlpatterns = [

    path('ws/newPendingTransactions/', consumers.InfuraWebSocketConsumer.as_asgi()),
]


application = ProtocolTypeRouter(
    {

        # for Websocket protocol
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    }
)
