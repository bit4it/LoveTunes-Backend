from django.urls import path
from . import consumers
print("urls")

websocket_urlpatterns = [
    path(r"ws/listening/session/<session_id>/", consumers.ChatConsumer.as_asgi()),
]