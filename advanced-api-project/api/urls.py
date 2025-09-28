from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

urlpatterns = [
    # API overview (accessible without authentication)
    path('', views.api_overview, name='api-overview'),
    
    # Authentication endpoint
    path('auth-token/', views.CustomObtainAuthToken.as_view(), name='api_token_auth'),
    
    # Route for the BookList view (ListAPIView)
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
]
