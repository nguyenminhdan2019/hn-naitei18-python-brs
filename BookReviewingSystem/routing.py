from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.conf.urls import url
from review.consumers import RatingConsumer
from notifications.consumers import NotificationConsumer
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
    	URLRouter([
			url(r'ws/review/books/(?P<id>\w+)/$', RatingConsumer),
			url(r'ws/notifications/$', NotificationConsumer),
			])
    )
})
