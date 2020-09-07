import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Book, Rating
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class RatingConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        print('tai sao cai nay lai ra duoc nhi',self.room_name)
        # Join room group
        print(self.room_name)
        self.group_name = 'book_'+ str(self.room_name)
        print("connect to group: ",self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        review = text_data_json['review']
        star = int(text_data_json['star'])
        userId = text_data_json['userId']
        bookId = text_data_json['bookId']
        
        user = User.objects.get(pk=userId)
        book = Book.objects.get(pk=bookId)

        review = Rating(user=user, book=book, star=star, review = review)
        print(review)
        review.save()
        html_render = render_to_string(template_name = 'include/rating.html', context={'rating': review})
        # print("send to : ", self.room_name)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'html_render': html_render,
                'message' : "Success"
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # print(message)
        html_render = event['html_render']
        self.send(text_data=json.dumps({
            'message': message,
            'html_render' : html_render
        }))
