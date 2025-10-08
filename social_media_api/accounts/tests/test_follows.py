# accounts/tests/test_follows.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class FollowFlowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.follow_url = lambda uid: reverse('follow-user', args=[uid])
        self.unfollow_url = lambda uid: reverse('unfollow-user', args=[uid])
        self.feed_url = reverse('feed')

    def test_follow_and_feed(self):
        self.client.login(username='alice', password='pass')
        # bob creates posts
        Post.objects.create(author=self.user2, content='Bob post 1')
        Post.objects.create(author=self.user2, content='Bob post 2')

        # initially, feed is empty (if include_self=true and alice has no posts, empty)
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

        # alice follows bob
        resp = self.client.post(self.follow_url(self.user2.pk))
        self.assertEqual(resp.status_code, 200)
        # feed should now contain bob's posts
        resp = self.client.get(self.feed_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data['results']) >= 2)

    def test_unfollow(self):
        self.client.login(username='alice', password='pass')
        self.client.post(self.follow_url(self.user2.pk))
        resp = self.client.post(self.unfollow_url(self.user2.pk))
        self.assertEqual(resp.status_code, 200)
