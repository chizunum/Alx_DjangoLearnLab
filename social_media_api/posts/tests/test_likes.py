from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeFlowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(author=self.user2, title='Hi', content='yo')

    def test_like_creates_like_and_notification(self):
        self.client.login(username='alice', password='pass')
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user1).exists())
        # Notification for post author
        self.assertTrue(Notification.objects.filter(recipient=self.user2, actor=self.user1, verb__icontains="liked").exists())

    def test_cannot_like_twice(self):
        self.client.login(username='alice', password='pass')
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        resp1 = self.client.post(url)
        resp2 = self.client.post(url)
        self.assertEqual(resp2.status_code, 400)
