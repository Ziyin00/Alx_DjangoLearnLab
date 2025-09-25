from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    Provides list, create, retrieve, update, and destroy actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def api_overview(request):
    """
    API Overview - List of available endpoints
    """
    api_urls = {
        'Books List (ListAPIView)': '/api/books/',
        'Books CRUD (ViewSet)': '/api/books_all/',
        'Admin Panel': '/admin/',
        'Django REST Framework Browsable API': '/api/books_all/',
    }
    return Response(api_urls)