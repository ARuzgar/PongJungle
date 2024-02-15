import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from blog.routing import websocket_urlpatterns 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogApp.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django'nun standart ASGI uygulaması, HTTP için
    "websocket": AuthMiddlewareStack(  # WebSocket bağlantıları için
        URLRouter(
            websocket_urlpatterns  # chat uygulamanızın WebSocket URL desenleri
        )
    ),
})
