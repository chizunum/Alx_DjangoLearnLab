from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()

class NotificationsTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='p')
        self.u2 = User.objects.create_user(username='u2', password='p')
        Notification.objects.create(recipient=self.u1, actor=self.u2, verb='followed you')

    def test_list_notifications(self):
        self.client.login(username='u1', password='p')
        resp = self.client.get(reverse('notifications-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
