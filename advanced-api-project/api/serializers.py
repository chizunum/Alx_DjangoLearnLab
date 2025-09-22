from rest_framework import serializers
from .models import Author, Book
import datetime


# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to prevent future publication years
    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. ({value})"
            )
        return value


# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to include books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
