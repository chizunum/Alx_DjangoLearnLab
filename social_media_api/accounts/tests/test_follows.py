from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class FollowFeedTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')

        # Bob's posts
        Post.objects.create(author=self.bob, title='B1', content='bob post 1')
        Post.objects.create(author=self.bob, title='B2', content='bob post 2')

        # URLs
        self.feed_url = '/api/posts/feed/'
        self.follow_url = f'/api/accounts/follow/{self.bob.pk}/'
        self.unfollow_url = f'/api/accounts/unfollow/{self.bob.pk}/'

    def test_follow_and_feed(self):
        """Ensure following a user populates the feed with their posts"""
        self.client.login(username='alice', password='pass')

        # Initially, feed should be empty (Alice follows no one)
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

        # Alice follows Bob
        follow_response = self.client.post(self.follow_url)
        self.assertEqual(follow_response.status_code, 200)

        # Now Alice should see Bob's posts in her feed
        feed_response = self.client.get(self.feed_url)
        self.assertEqual(feed_response.status_code, 200)
        self.assertGreaterEqual(len(feed_response.data['results']), 2)

    def test_unfollow_removes_feed_posts(self):
        """Ensure unfollowing removes user's posts from feed"""
        self.client.login(username='alice', password='pass')
        self.client.post(self.follow_url)

        # Feed should have Bob's posts after following
        response = self.client.get(self.feed_url)
        self.assertGreaterEqual(len(response.data['results']), 2)

        # Unfollow Bob
        unfollow_response = self.client.post(self.unfollow_url)
        self.assertEqual(unfollow_response.status_code, 200)

        # Feed should now be empty
        response = self.client.get(self.feed_url)
        self.assertEqual(len(response.data['results']), 0)
