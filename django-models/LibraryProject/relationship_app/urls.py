from django.urls import path
from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("books/", list_books.list_books, name="list_books"),  # Function-based view
    path("library/<int:pk>/", LibraryDetailView.LibraryDetailView.as_view(), name="library_detail"),  # Class-based view
]

# LibraryProject/urls.py


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
]
