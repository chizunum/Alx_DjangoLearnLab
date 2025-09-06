from django.urls import path
from . import views
from .views import list_books, login_view, logout_view

urlpatterns = [
    path("books/", views.list_books, name="list_books"),  # function-based view
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),  # class-based view
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
