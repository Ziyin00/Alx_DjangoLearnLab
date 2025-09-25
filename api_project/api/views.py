from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def api_overview(request):
    """
    API Overview - List of available endpoints
    """
    api_urls = {
        'Books API': '/api/books/',
        'Admin Panel': '/admin/',
        'Django REST Framework Browsable API': '/api/books/',
    }
    return Response(api_urls)