from django.urls import path
from . import views


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


    # Comments
    path('posts/<int:post_pk>/comments/', views.CommentListView.as_view(), name='comment_list'),
    path('posts/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_pk>/comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('posts/<int:post_pk>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]

