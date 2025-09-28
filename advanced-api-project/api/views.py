from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    This view provides read-only access to all books in the database.
    No authentication required for read access.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Custom queryset with author information to optimize database queries.
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
    ListView for retrieving all authors with their books.
    
    This view provides read-only access to all authors and their related books.
    No authentication required for read access.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


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