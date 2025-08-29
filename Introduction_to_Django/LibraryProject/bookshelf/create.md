# Create Book

```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Output: <Book: 1984 by George Orwell (1949)>

### `retrieve.md`
```markdown
# Retrieve Book

```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# Output: ('1984', 'George Orwell', 1949)

### `update.md`
```markdown
# Update Book

```python
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# Output: 'Nineteen Eighty-Four'

### `delete.md`
```markdown
# Delete Book

```python
book.delete()
Book.objects.all()
# Output: <QuerySet []>

---

