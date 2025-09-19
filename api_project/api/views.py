# api/views.py

# -----------------------------------------------------------
# Authentication & Permissions Setup:
# 1. Token authentication is enabled in settings.py.
# 2. Users retrieve their token via POST to /api/token/ with username/password.
# 3. Requests to these endpoints must include the token in the header:
#      Authorization: Token <your-token>
# 4. Permissions are enforced per viewset:
#      - IsAuthenticated: any logged-in user can access
#      - IsAdminUser: only admin/staff users can access
# -----------------------------------------------------------

from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Example: any authenticated user can access books
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require login

# Example: only admins can access authors
from .models import Author
from .serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins

from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, permissions


# Create your views here.


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()          # get all books
    serializer_class = BookSerializer      # use the serializer we just created

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()              # get all books
    serializer_class = BookSerializer    
    permission_classes = [permissions.IsAuthenticated]  # Require login

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user