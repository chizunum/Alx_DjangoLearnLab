from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm
from django.db.models import Q

# Create your views here.


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    q = request.GET.get("q", "").strip()
    books = Book.objects.all()
    if q:
        # Use ORM lookups, not raw SQL or string formatting
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, "bookshelf/book_list.html", {"books": books, "q": q})

@permission_required("bookshelf.can_create", raise_exception=True)
def add_book_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/add_book.html", {"form": form})

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/edit_book.html", {"form": form, "book": book})

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/confirm_delete.html", {"book": book})