# blog/urls.py
from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView, CommentListView,
    TagPostListView,  # 👈 import it
)
app_name = "blog"

urlpatterns = [
    # --- Auth ---
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # --- Blog CRUD ---
    path("", views.PostListView.as_view(), name="post-list"),  # Home = posts list
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # --- Comments ---
    path("post/<int:post_pk>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_edit"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),
    path("post/<int:post_pk>/comments/", views.CommentListView.as_view(), name="comment_list"),

    # --- Search & Tags ---
    path("search/", views.search_posts, name="search_posts"),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),
]