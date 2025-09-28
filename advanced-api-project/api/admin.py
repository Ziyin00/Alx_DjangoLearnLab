from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.
    
    Provides a user-friendly interface for managing authors in the Django admin.
    Includes list display, filtering, and search capabilities.
    """
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    
    Provides a user-friendly interface for managing books in the Django admin.
    Includes list display, filtering, and search capabilities with proper
    foreign key relationship handling.
    """
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')
    ordering = ('title',)
    list_select_related = ('author',)