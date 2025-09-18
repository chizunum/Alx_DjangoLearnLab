from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
# Create your views here.


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()          # get all books
    serializer_class = BookSerializer      # use the serializer we just created
