from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('books/', views.BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path('', include(router.urls)),
]
