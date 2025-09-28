from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    Provides list, create, retrieve, update, and destroy actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_overview(request):
    """
    API Overview - List of available endpoints
    """
    api_urls = {
        'Authentication': {
            'Get Token': '/api/auth-token/',
            'Note': 'Send POST request with username and password to get token',
        },
        'Books API (Requires Authentication)': {
            'Books List (ListAPIView)': '/api/books/',
            'Books CRUD (ViewSet)': '/api/books_all/',
        },
        'Other Endpoints': {
            'Admin Panel': '/admin/',
            'Django REST Framework Browsable API': '/api/books_all/',
        },
        'Authentication Header': {
            'Format': 'Authorization: Token <your-token-here>',
            'Example': 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
        }
    }
    return Response(api_urls)