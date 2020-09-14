from django.test import TestCase
from notifications.models import Notification
from django.contrib.auth.models import User

class NotificationTestCase(TestCase):
    @classmethod
    def setUp(self):
        user1 = User.objects.create(username = 'minhdan222', password='111222')
        user2 = User.objects.create(username='minhdan333', password='111222')
        notify = Notification.objects.create(sender=user1, user=user2, notification_type=2)

    def test_get_str(self):
        user1 = User.objects.get(username = 'minhdan222', password='111222')
        user2 = User.objects.get(username='minhdan333', password='111222')
        notify = Notification.objects.get(sender=user1, user=user2)
        self.assertEqual(notify.__str__(), 'minhdan222 to minhdan333')
    
    def test_text_preview_max_length(self):
        user1 = User.objects.get(username = 'minhdan222', password='111222')
        user2 = User.objects.get(username='minhdan333', password='111222')
        notify = Notification.objects.get(sender=user1, user=user2)
        max_length = notify._meta.get_field('text_preview').max_length
        self.assertEqual(max_length, 90)


