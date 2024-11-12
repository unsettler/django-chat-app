import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chattrapp import consumers
from channels.layers import get_channel_layer
from chattrapp.routing import websocket_urlpatterns
import chattrapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chattr.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chattrapp.routing.websocket_urlpatterns
        )
    ),
})
channel_layer = get_channel_layer()