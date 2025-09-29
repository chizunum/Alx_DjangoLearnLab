from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # example: home page view — make sure you have this view
    path("", views.home, name="home"),  # ensure you have a home view; or adjust

    # auth
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("", views.PostListView.as_view(), name="posts-list"),
    path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
]
