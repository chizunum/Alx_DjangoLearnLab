# social_media_api

A simple starter Social Media API using Django and Django REST Framework.

## Setup

1. Create virtual environment and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # or:
   pip install django djangorestframework djangorestframework-authtoken
### Posts
- `GET /api/posts/` — list posts (params: page, page_size, search, ordering, author__username)
- `POST /api/posts/` — create (auth required)
- `GET /api/posts/{id}/` — retrieve
- `PUT/PATCH /api/posts/{id}/` — update (owner only)
- `DELETE /api/posts/{id}/` — delete (owner only)

### Comments
- `GET /api/comments/` — list (filter by ?post=ID)
- `POST /api/comments/` — create (auth required)
- `GET /api/comments/{id}/` — retrieve
- `PUT/PATCH /api/comments/{id}/` — update (owner only)
- `DELETE /api/comments/{id}/` — delete (owner only)
