from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework


# Create your views here.



# List all books (anyone can read)
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of all books.
    Accessible by anyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching fields (text lookup)
    search_fields = ['title', 'author']

    # Ordering fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


# Retrieve details of a single book
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<id>/
    Returns details of a single book by ID.
    Accessible by anyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book (only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Creates a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Example rule: block books with future publication year
        year = serializer.validated_data.get("publication_year")
        current_year = datetime.now().year
        if year > current_year:
            raise ValidationError("Publication year cannot be in the future.")

        # Example: if Book has created_by field, attach logged-in user
        # serializer.save(created_by=self.request.user)

        serializer.save()

# Update a book (only for authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<id>/update/
    Updates an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Example: enforce rule before updating
        title = serializer.validated_data.get("title")
        if title and len(title) < 3:
            raise ValidationError("Book title must be at least 3 characters long.")
        
        serializer.save()


# Delete a book (only for authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<id>/delete/
    Deletes a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
