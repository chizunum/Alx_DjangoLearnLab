from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from posts.models import Post

# Create your tests here.


User = get_user_model()

class PostsApiTests(APITestCase):
    def setUp(self):
        # create user and token
        self.user = User.objects.create_user(username="alice", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_post(self):
        """Test that a logged-in user can create a post"""
        data = {"title": "My First Post", "content": "This is the content"}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])

    def test_get_posts(self):
        """Test that posts can be retrieved"""
        Post.objects.create(author=self.user, title="Post 1", content="Content")
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["results"]), 1)
