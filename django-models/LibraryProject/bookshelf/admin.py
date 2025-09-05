from django.contrib import admin
from .models import Book

# Customize how the Book model appears in the admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Filters in the sidebar
    list_filter = ('publication_year', 'author')
    
    # Search bar fields
    search_fields = ('title', 'author')
