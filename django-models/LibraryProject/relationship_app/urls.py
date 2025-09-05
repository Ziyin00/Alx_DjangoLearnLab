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
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # authentication
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # role-based access
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("librarian-dashboard/", librarian_dashboard, name="librarian_dashboard"),
    path("member-dashboard/", member_dashboard, name="member_dashboard"),

    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
]

# LibraryProject/urls.py


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
]
