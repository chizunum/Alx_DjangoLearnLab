from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from .models import Library, Book


# Function-based view to list all books (renders template)
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
