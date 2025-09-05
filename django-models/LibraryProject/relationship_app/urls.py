from django.urls import path

from django.contrib import admin
from django.urls import path, include

from . import views
from .views import list_books, LibraryDetailView
from .admin_view import admin_dashboard
from .librarian_view import librarian_dashboard
from .member_view import member_dashboard
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Book management URLs
    path("books/add/", views.add_book, name="add_book"),          # <-- contains "add_book/"
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),  # <-- contains "edit_book/"
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
    
    # Other URLs
    path("books/", views.list_books, name="book_list"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Role-based dashboards
    path("admin-dashboard/", views.admin_view, name="admin_dashboard"),
    path("librarian-dashboard/", views.librarian_view, name="librarian_dashboard"),
    path("member-dashboard/", views.member_view, name="member_dashboard"),
]

# LibraryProject/urls.py


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
]
