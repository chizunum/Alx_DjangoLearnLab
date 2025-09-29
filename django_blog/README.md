Routes:

GET / → posts list

GET /posts/new/ → create (auth required)

GET /posts/<pk>/ → detail

GET /posts/<pk>/edit/ → edit (author only)

GET /posts/<pk>/delete/ → delete (author only)

Auth: Login required for create/edit/delete. Use Django admin or your auth views for user management.

Templates: located in blog/templates/blog/.

Forms: PostForm located in blog/forms.py.