from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

        # Create author instances instead of plain strings
        self.author1 = Author.objects.create(name="Author A")
        self.author2 = Author.objects.create(name="Author B")

        # Use the Author instances for books
        self.book1 = Book.objects.create(
            title="Book One", author=self.author1, publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two", author=self.author2, publication_year=2019
        )

    # ---------------- LIST & DETAIL ----------------

    def test_list_books(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], self.book1.title)

