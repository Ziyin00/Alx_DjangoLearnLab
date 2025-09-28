"""
Custom filters for the API views.
This module provides filtering capabilities for the Book and Author models.
"""

import django_filters
from django.db.models import Q, Count
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for Book model.
    
    Provides comprehensive filtering options for books including:
    - Title filtering (exact match and contains)
    - Author filtering (by name and ID)
    - Publication year filtering (exact, range, and comparison)
    - Combined filtering capabilities
    """
    
    # Title filtering options
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', help_text='Filter by title (case-insensitive)')
    title_exact = django_filters.CharFilter(field_name='title', lookup_expr='exact', help_text='Filter by exact title match')
    
    # Author filtering options
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', help_text='Filter by author name (case-insensitive)')
    author_id = django_filters.NumberFilter(field_name='author__id', help_text='Filter by author ID')
    author = django_filters.CharFilter(method='filter_by_author', help_text='Filter by author name or ID')
    
    # Publication year filtering options
    publication_year = django_filters.NumberFilter(field_name='publication_year', help_text='Filter by exact publication year')
    publication_year_min = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte', help_text='Filter by minimum publication year')
    publication_year_max = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte', help_text='Filter by maximum publication year')
    publication_year_range = django_filters.RangeFilter(field_name='publication_year', help_text='Filter by publication year range (e.g., ?publication_year_range_min=1900&publication_year_range_max=2000)')
    
    # Combined search functionality
    search = django_filters.CharFilter(method='filter_search', help_text='Search across title and author name')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def filter_by_author(self, queryset, name, value):
        """
        Custom filter method to search by author name or ID.
        
        Args:
            queryset: The queryset to filter
            name: The field name
            value: The search value (can be author name or ID)
            
        Returns:
            Filtered queryset
        """
        try:
            # Try to filter by author ID if value is numeric
            author_id = int(value)
            return queryset.filter(author__id=author_id)
        except (ValueError, TypeError):
            # If not numeric, filter by author name
            return queryset.filter(author__name__icontains=value)
    
    def filter_search(self, queryset, name, value):
        """
        Custom search method to search across multiple fields.
        
        Args:
            queryset: The queryset to search
            name: The field name
            value: The search value
            
        Returns:
            Filtered queryset
        """
        return queryset.filter(
            Q(title__icontains=value) |
            Q(author__name__icontains=value)
        )


class AuthorFilter(django_filters.FilterSet):
    """
    Custom filter class for Author model.
    
    Provides filtering options for authors including:
    - Name filtering (exact match and contains)
    - Book count filtering
    - Combined search functionality
    """
    
    # Name filtering options
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', help_text='Filter by author name (case-insensitive)')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact', help_text='Filter by exact author name match')
    
    # Book count filtering
    book_count_min = django_filters.NumberFilter(method='filter_min_book_count', help_text='Filter authors with minimum number of books')
    book_count_max = django_filters.NumberFilter(method='filter_max_book_count', help_text='Filter authors with maximum number of books')
    
    # Combined search functionality
    search = django_filters.CharFilter(method='filter_search', help_text='Search across author name and book titles')
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_min_book_count(self, queryset, name, value):
        """
        Filter authors with minimum number of books.
        
        Args:
            queryset: The queryset to filter
            name: The field name
            value: The minimum book count
            
        Returns:
            Filtered queryset
        """
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    def filter_max_book_count(self, queryset, name, value):
        """
        Filter authors with maximum number of books.
        
        Args:
            queryset: The queryset to filter
            name: The field name
            value: The maximum book count
            
        Returns:
            Filtered queryset
        """
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__lte=value)
    
    def filter_search(self, queryset, name, value):
        """
        Custom search method to search across author name and book titles.
        
        Args:
            queryset: The queryset to search
            name: The field name
            value: The search value
            
        Returns:
            Filtered queryset
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(books__title__icontains=value)
        ).distinct()
