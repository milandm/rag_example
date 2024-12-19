from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.urls import re_path
from text_bot.views.consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         # path("ws/chat/", ChatConsumer.as_asgi()),
#     ])
# })

# websocket_urlpatterns = [
#     re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})