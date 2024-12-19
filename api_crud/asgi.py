"""
ASGI config for ir project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter
# from api_crud.routing import application as websocket_application
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_crud.settings')
# django.setup()
# # application = get_asgi_application()
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # Standard HTTP routing
#     "websocket": websocket_application,  # WebSocket routing
# })

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from api_crud.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_crud.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Standard HTTP routing
    "websocket": URLRouter(websocket_urlpatterns),  # WebSocket routing
})