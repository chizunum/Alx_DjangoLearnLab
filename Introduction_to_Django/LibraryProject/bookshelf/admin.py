from django.contrib import admin
from .models import Book


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # shows these columns in list view
    list_filter = ("publication_year", "author")            # filters on the right sidebar
    search_fields = ("title", "author")                     # search box