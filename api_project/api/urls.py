from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter



# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Still keep the ListAPIView endpoint if you want
    path('books/', BookList.as_view(), name='book-list'),

    # Include router-generated routes (CRUD endpoints)
    path('', include(router.urls)),
]
