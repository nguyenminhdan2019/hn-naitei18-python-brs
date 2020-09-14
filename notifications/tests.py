from django.test import TestCase
from notifications.models import Notification
from django.contrib.auth.models import User
from django.urls import reverse
from .views import ShowNOtifications, DeleteNotification, CountNotifications
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

class NotificationsViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        user1 = User.objects.create(username = 'minhdan222', password='111222')
        user2 = User.objects.create(username='minhdan333', password='111222')
        Notification.objects.create(sender=user1, user=user2, notification_type=2)

    def test_show_notifications(self):
    
        self.client.login(username='minhdan333', password='111222')
        # response = self.client.get(reverse('show-notifications'))
        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, 302)


    def test_delete_notifications(self):

        self.client.login(username='minhdan333', password='111222')
        
        user2 = User.objects.get(username='minhdan333', password='111222')
        Notification.objects.create(sender=user1, user=user2, notification_type=2)
        # response = self.client.get(reverse('show-notifications'))
        response = self.client.post('/notifications/1/delete')

        self.assertEqual(response.status_code, 302)

    def test_count_notifications(self):
        self.client.login(username='minhdan333', password='111222')
        user2 = User.objects.get(username='minhdan333', password='111222')

        Notification.objects.create(sender=user1, user=user2, notification_type=2)

        response = self.client.get(reverse('show-notifications'))
        self.assertQuerysetEqual(response.context['count_notifications'], 1)
