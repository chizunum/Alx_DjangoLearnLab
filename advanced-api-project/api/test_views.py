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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_authenticated(self):
    # ✅ Login the test user instead of force_authenticate
    self.client.login(username="testuser", password="password123")

    url = reverse("book-create")
    author = Author.objects.create(name="Author C")

    payload = {
        "title": "New Book",
        "author": author.id,
        "publication_year": 2025,
    }

    response = self.client.post(url, payload, format="json")

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book_authenticated(self):
    # ✅ use login instead of force_authenticate
    self.client.login(username="testuser", password="password123")

    url = reverse("book-update", kwargs={"pk": self.book2.pk})
    payload = {
        "title": "Book Two Updated",
        "author": self.book2.author.id,
        "publication_year": self.book2.publication_year,
    }

    response = self.client.patch(url, payload, format="json")

    self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
    self.book2.refresh_from_db()
    self.assertEqual(self.book2.title, "Book Two Updated")


    def test_delete_book_authenticated(self):
    # ✅ login the test user
    self.client.login(username="testuser", password="password123")

    author = Author.objects.create(name="Temp Author")
    b = Book.objects.create(title="Temp Book", author=author, publication_year=2000)

    url = f"/api/books/{b.id}/delete/"
    response = self.client.delete(url)

    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(Book.objects.filter(id=b.id).exists())  # ✅ verify book is gone


    def test_delete_book_unauthenticated(self):
    author = Author.objects.create(name="Temp Author 2")
    b = Book.objects.create(title="Another Temp", author=author, publication_year=1999)

    url = f"/api/books/{b.id}/delete/"
    response = self.client.delete(url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertTrue(Book.objects.filter(id=b.id).exists())  # ✅ still in DB



      



