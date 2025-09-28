from django.urls import path
from . import views

urlpatterns = [
    # API overview (accessible without authentication)
    path('', views.api_overview, name='api-overview'),
    
    # Authentication endpoint
    path('auth-token/', views.CustomObtainAuthToken.as_view(), name='api_token_auth'),
    
    # Books API endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Authors API endpoints (read-only)
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
