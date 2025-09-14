# Update Book

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> book.title, book.author, book.publication_year
('1984', 'George Orwell', 1949)

>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

>>> book.title
'Nineteen Eighty-Four'
