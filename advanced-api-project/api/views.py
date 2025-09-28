from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter, AuthorFilter


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with advanced query capabilities.
    
    This view provides read-only access to all books in the database with:
    - Filtering: Filter by title, author, publication year
    - Searching: Search across title and author name
    - Ordering: Sort by any field (title, publication_year, author__name)
    - Pagination: Results are paginated (10 items per page)
    
    No authentication required for read access.
    
    Query Parameters:
    - Filtering:
      * title: Filter by title (case-insensitive contains)
      * title_exact: Filter by exact title match
      * author_name: Filter by author name (case-insensitive contains)
      * author_id: Filter by author ID
      * author: Filter by author name or ID
      * publication_year: Filter by exact publication year
      * publication_year_min: Filter by minimum publication year
      * publication_year_max: Filter by maximum publication year
      * publication_year_range_min: Start of publication year range
      * publication_year_range_max: End of publication year range
      * search: Search across title and author name
    
    - Ordering:
      * ordering: Sort by field (e.g., 'title', '-publication_year', 'author__name')
      * Available fields: title, publication_year, author__name, author__id
    
    - Pagination:
      * page: Page number
      * page_size: Number of items per page (max 100)
    
    Examples:
    - GET /api/books/?title=harry
    - GET /api/books/?author_name=rowling
    - GET /api/books/?publication_year_min=1990&publication_year_max=2000
    - GET /api/books/?search=potter
    - GET /api/books/?ordering=-publication_year
    - GET /api/books/?page=2&page_size=5
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Advanced query capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name', 'author__id']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Custom queryset with author information to optimize database queries.
        Includes filtering, searching, and ordering capabilities.
        """
        return Book.objects.select_related('author').all()


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    This view provides read-only access to a specific book.
    No authentication required for read access.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    This view handles book creation with proper validation.
    Authentication required for write operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom method to handle book creation with additional logic.
        """
        # Add any custom logic here before saving
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to provide custom response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Book created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    This view handles both partial and full updates of book data.
    Authentication required for write operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """
        Custom method to handle book updates with additional logic.
        """
        # Add any custom logic here before saving
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to provide custom response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Book updated successfully',
            'data': serializer.data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    This view handles book deletion with proper confirmation.
    Authentication required for write operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """
        Custom method to handle book deletion with additional logic.
        """
        # Add any custom logic here before deletion
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide custom response.
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Book "{book_title}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books and advanced query capabilities.
    
    This view provides read-only access to all authors and their related books with:
    - Filtering: Filter by name, book count
    - Searching: Search across author name and book titles
    - Ordering: Sort by name or book count
    - Pagination: Results are paginated (10 items per page)
    
    No authentication required for read access.
    
    Query Parameters:
    - Filtering:
      * name: Filter by author name (case-insensitive contains)
      * name_exact: Filter by exact author name match
      * book_count_min: Filter authors with minimum number of books
      * book_count_max: Filter authors with maximum number of books
      * search: Search across author name and book titles
    
    - Ordering:
      * ordering: Sort by field (e.g., 'name', '-name')
      * Available fields: name, id
    
    - Pagination:
      * page: Page number
      * page_size: Number of items per page (max 100)
    
    Examples:
    - GET /api/authors/?name=rowling
    - GET /api/authors/?book_count_min=2
    - GET /api/authors/?search=potter
    - GET /api/authors/?ordering=name
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    # Advanced query capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name', 'books__title']
    ordering_fields = ['name', 'id']
    ordering = ['name']  # Default ordering


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with their books.
    
    This view provides read-only access to a specific author and their books.
    No authentication required for read access.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom token authentication view that returns user information along with the token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_overview(request):
    """
    API Overview - List of available endpoints with detailed documentation.
    """
    api_urls = {
        'Authentication': {
            'Get Token': '/api/auth-token/',
            'Note': 'Send POST request with username and password to get token',
        },
        'Books API': {
            'List Books (Read-only)': '/api/books/',
            'Book Detail (Read-only)': '/api/books/<id>/',
            'Create Book (Authenticated)': '/api/books/create/',
            'Update Book (Authenticated)': '/api/books/<id>/update/',
            'Delete Book (Authenticated)': '/api/books/<id>/delete/',
        },
        'Authors API': {
            'List Authors (Read-only)': '/api/authors/',
            'Author Detail (Read-only)': '/api/authors/<id>/',
        },
        'Advanced Query Capabilities': {
            'Filtering': {
                'Books': 'Filter by title, author, publication year',
                'Authors': 'Filter by name, book count',
                'Examples': [
                    '/api/books/?title=harry',
                    '/api/books/?author_name=rowling',
                    '/api/books/?publication_year_min=1990',
                    '/api/authors/?name=rowling',
                    '/api/authors/?book_count_min=2'
                ]
            },
            'Searching': {
                'Books': 'Search across title and author name',
                'Authors': 'Search across author name and book titles',
                'Examples': [
                    '/api/books/?search=potter',
                    '/api/authors/?search=harry'
                ]
            },
            'Ordering': {
                'Books': 'Sort by title, publication_year, author__name',
                'Authors': 'Sort by name, id',
                'Examples': [
                    '/api/books/?ordering=-publication_year',
                    '/api/books/?ordering=title',
                    '/api/authors/?ordering=name'
                ]
            },
            'Pagination': {
                'Default': '10 items per page',
                'Custom': 'Use ?page=N&page_size=M',
                'Examples': [
                    '/api/books/?page=2',
                    '/api/books/?page=1&page_size=5'
                ]
            }
        },
        'Other Endpoints': {
            'Admin Panel': '/admin/',
            'API Overview': '/api/',
        },
        'Authentication Header': {
            'Format': 'Authorization: Token <your-token-here>',
            'Example': 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
        },
        'HTTP Methods': {
            'GET': 'Read operations (no auth required)',
            'POST': 'Create operations (auth required)',
            'PUT/PATCH': 'Update operations (auth required)',
            'DELETE': 'Delete operations (auth required)',
        }
    }
    return Response(api_urls)