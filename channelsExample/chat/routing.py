
from django.urls import path
from chat.consumers import ChatConsumer
 
websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
]