import django
import os

# Setup Django (needed if running script outside manage.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def run_queries():
    # Query 1: All books by a specific author
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
    except Author.DoesNotExist:
        print(f"No author found with name {author_name}")

    # Query 2: List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"No library found with name {library_name}")

    # Query 3: Retrieve the librarian for a library
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"The librarian of {library_name} is {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}")


if __name__ == "__main__":
    run_queries()
