from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
	NOTIFICATION_TYPES = ((1,'Request'), (2,'Follow'))
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
	text_preview = models.CharField(max_length=90, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)

	def __str__(self):
		return '{} to {}'.format(self.sender, self.user)

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
import json
from django.template import loader

def create_new_folow_notifications(sender, **kwargs):
	notify = kwargs['instance']
	# print(notify)
	channel_layer = get_channel_layer()
	# room_name = 'user_' + str(notify.user.id)
	room_name = 'group1'

	my_dictionary = {
		'pk': notify.pk,
		'sender': notify.sender.username,
		'to_user': notify.user.username,
		'notification_type': notify.notification_type,
		'text_preview': notify.text_preview,
		'date': notify.date,
		'is_seen': notify.is_seen,
	}

	# print(my_dictionary)
	message = json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
	if notify.notification_type == 1 : 
		html_render = render_to_string('includes/requestNotification.html',context={'notification': notify})
	else: 
		html_render = render_to_string('includes/followNotification.html',context={'notification': notify})
	
	async_to_sync(channel_layer.group_send)(
		'group1', {
            'type': 'chat_message',
            'message': message,
			'html_render' : html_render
		}
	)

post_save.connect(create_new_folow_notifications, sender=Notification)
