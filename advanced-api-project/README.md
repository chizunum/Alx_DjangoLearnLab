# Advanced API Project

## Views

### BookListView
- **Endpoint:** `/api/books/`
- **Method:** GET
- **Access:** Public
- **Description:** Returns a list of all books.

### BookDetailView
- **Endpoint:** `/api/books/<id>/`
- **Method:** GET
- **Access:** Public
- **Description:** Returns details of a single book.

### BookCreateView
- **Endpoint:** `/api/books/create/`
- **Method:** POST
- **Access:** Authenticated users only
- **Description:** Creates a new book entry.

### BookUpdateView
- **Endpoint:** `/api/books/<id>/update/`
- **Method:** PUT/PATCH
- **Access:** Authenticated users only
- **Description:** Updates an existing book.

### BookDeleteView
- **Endpoint:** `/api/books/<id>/delete/`
- **Method:** DELETE
- **Access:** Authenticated users only
- **Description:** Deletes a book.

### Filtering
- `/api/books/?author=Rowling`
- `/api/books/?publication_year=2005`

### Searching
- `/api/books/?search=Harry`

### Ordering
- `/api/books/?ordering=title`
- `/api/books/?ordering=-publication_year`
