import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from posts.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta_clone.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
    ]),
})