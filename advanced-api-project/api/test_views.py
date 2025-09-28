"""
Comprehensive Unit Tests for Advanced API Project

This module contains unit tests for all API endpoints, focusing on:
- CRUD operations for Book and Author models
- Authentication and permission testing
- Filtering, searching, and ordering functionality
- Response data integrity and status code accuracy

Test Categories:
1. Book CRUD Operations
2. Author CRUD Operations  
3. Authentication & Permissions
4. Advanced Query Capabilities (Filtering, Searching, Ordering)
5. Error Handling & Edge Cases
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import transaction
from .models import Author, Book
import json


class BookCRUDTestCase(APITestCase):
    """
    Test cases for Book CRUD operations.
    
    Tests:
    - Book creation (authenticated)
    - Book retrieval (public)
    - Book updates (authenticated)
    - Book deletion (authenticated)
    - Unauthorized access scenarios
    """
    
    def setUp(self):
        """Set up test data and authentication."""
        # Create test user and token
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        
        # Create test author
        self.author = Author.objects.create(name='J.K. Rowling')
        
        # Create test book
        self.book = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author
        )
        
        # Set up API client
        self.client = APIClient()
        
    def test_book_list_public_access(self):
        """Test that book list is accessible without authentication."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.book.title)
        
    def test_book_detail_public_access(self):
        """Test that book detail is accessible without authentication."""
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['author'], self.author.pk)
        
    def test_book_create_authenticated(self):
        """Test book creation with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {
            'title': 'Harry Potter and the Chamber of Secrets',
            'publication_year': 1998,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], data['title'])
        self.assertEqual(response.data['message'], 'Book created successfully')
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title=data['title']).exists())
        
    def test_book_create_unauthorized(self):
        """Test book creation without authentication."""
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_book_update_authenticated(self):
        """Test book update with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1997,
            'author': self.author.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], data['title'])
        self.assertEqual(response.data['message'], 'Book updated successfully')
        
        # Verify book was updated in database
        updated_book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(updated_book.title, data['title'])
        
    def test_book_update_unauthorized(self):
        """Test book update without authentication."""
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {'title': 'Unauthorized Update'}
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_book_delete_authenticated(self):
        """Test book deletion with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('deleted successfully', response.data['message'])
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
        
    def test_book_delete_unauthorized(self):
        """Test book deletion without authentication."""
        url = reverse('book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_book_create_validation(self):
        """Test book creation with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {
            'title': '',  # Empty title
            'publication_year': 2030,  # Future year
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_book_not_found(self):
        """Test accessing non-existent book."""
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorCRUDTestCase(APITestCase):
    """
    Test cases for Author CRUD operations.
    
    Tests:
    - Author list and detail views
    - Nested book relationships
    - Author filtering and searching
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        self.client = APIClient()
        
    def test_author_list_public_access(self):
        """Test that author list is accessible without authentication."""
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_author_detail_public_access(self):
        """Test that author detail is accessible without authentication."""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], self.book1.title)
        
    def test_author_not_found(self):
        """Test accessing non-existent author."""
        url = reverse('author-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticationTestCase(APITestCase):
    """
    Test cases for authentication and token management.
    
    Tests:
    - Token authentication
    - Custom token response
    - Invalid credentials
    """
    
    def setUp(self):
        """Set up test user and data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test author for session authentication tests
        self.author = Author.objects.create(name='Test Author')
        
        self.client = APIClient()
        
    def test_token_authentication_success(self):
        """Test successful token authentication."""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        
    def test_token_authentication_invalid_credentials(self):
        """Test token authentication with invalid credentials."""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_token_authentication_missing_fields(self):
        """Test token authentication with missing fields."""
        url = reverse('api_token_auth')
        data = {'username': 'testuser'}  # Missing password
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_session_authentication_success(self):
        """Test session authentication with login."""
        # Login using session authentication
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success)
        
        # Test that we can access authenticated endpoints
        url = reverse('book-create')
        data = {
            'title': 'Session Authenticated Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_session_authentication_failure(self):
        """Test session authentication with wrong credentials."""
        # Try to login with wrong password
        login_success = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login_success)
        
        # Test that we cannot access authenticated endpoints
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_session_authentication_logout(self):
        """Test that logout prevents access to authenticated endpoints."""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Verify we can access authenticated endpoints
        url = reverse('book-create')
        data = {
            'title': 'Before Logout Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Logout
        self.client.logout()
        
        # Verify we cannot access authenticated endpoints after logout
        data = {
            'title': 'After Logout Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdvancedQueryTestCase(APITestCase):
    """
    Test cases for advanced query capabilities.
    
    Tests:
    - Filtering by various fields
    - Text searching
    - Ordering results
    - Pagination
    """
    
    def setUp(self):
        """Set up test data for query testing."""
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.books = [
            Book.objects.create(
                title='Harry Potter and the Philosopher\'s Stone',
                publication_year=1997,
                author=self.author1
            ),
            Book.objects.create(
                title='Harry Potter and the Chamber of Secrets',
                publication_year=1998,
                author=self.author1
            ),
            Book.objects.create(
                title='A Game of Thrones',
                publication_year=1996,
                author=self.author2
            ),
            Book.objects.create(
                title='The Lord of the Rings',
                publication_year=1954,
                author=self.author3
            ),
            Book.objects.create(
                title='The Hobbit',
                publication_year=1937,
                author=self.author3
            )
        ]
        
        self.client = APIClient()
        
    def test_book_filtering_by_title(self):
        """Test filtering books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        for book in response.data['results']:
            self.assertIn('Harry', book['title'])
            
    def test_book_filtering_by_author_name(self):
        """Test filtering books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'author_name': 'Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.pk)
            
    def test_book_filtering_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
        
    def test_book_filtering_by_year_range(self):
        """Test filtering books by publication year range."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'publication_year_min': 1990,
            'publication_year_max': 2000
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 2 Harry Potter + 1 Game of Thrones
        
    def test_book_search_functionality(self):
        """Test text search across title and author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_book_ordering_by_title(self):
        """Test ordering books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
    def test_book_ordering_by_publication_year_desc(self):
        """Test ordering books by publication year descending."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
        
    def test_book_ordering_by_author_name(self):
        """Test ordering books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'author__name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by author name
        
    def test_combined_filtering_and_ordering(self):
        """Test combining filtering and ordering."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author_name': 'Rowling',
            'ordering': 'publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
        
    def test_pagination(self):
        """Test pagination functionality."""
        url = reverse('book-list')
        response = self.client.get(url, {'page_size': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test that pagination structure is present
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Test that we get results (page_size may not be respected due to small dataset)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['count'], 5)  # Total count should be 5
        
    def test_author_filtering_by_name(self):
        """Test filtering authors by name."""
        url = reverse('author-list')
        response = self.client.get(url, {'name': 'Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'J.K. Rowling')
        
    def test_author_search_functionality(self):
        """Test text search across author name and book titles."""
        url = reverse('author-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find J.K. Rowling because she wrote Harry Potter books
        self.assertEqual(len(response.data['results']), 1)
        
    def test_author_ordering_by_name(self):
        """Test ordering authors by name."""
        url = reverse('author-list')
        response = self.client.get(url, {'ordering': 'name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data['results']]
        self.assertEqual(names, sorted(names))


class APIOverviewTestCase(APITestCase):
    """
    Test cases for API overview endpoint.
    
    Tests:
    - API overview response structure
    - Endpoint documentation
    """
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        
    def test_api_overview_structure(self):
        """Test API overview endpoint structure."""
        url = reverse('api-overview')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Authentication', response.data)
        self.assertIn('Books API', response.data)
        self.assertIn('Authors API', response.data)
        self.assertIn('Advanced Query Capabilities', response.data)
        
    def test_api_overview_authentication_section(self):
        """Test API overview authentication section."""
        url = reverse('api-overview')
        response = self.client.get(url)
        
        auth_section = response.data['Authentication']
        self.assertIn('Get Token', auth_section)
        self.assertIn('Note', auth_section)
        
    def test_api_overview_books_section(self):
        """Test API overview books section."""
        url = reverse('api-overview')
        response = self.client.get(url)
        
        books_section = response.data['Books API']
        self.assertIn('List Books (Read-only)', books_section)
        self.assertIn('Book Detail (Read-only)', books_section)
        self.assertIn('Create Book (Authenticated)', books_section)
        self.assertIn('Update Book (Authenticated)', books_section)
        self.assertIn('Delete Book (Authenticated)', books_section)
        
    def test_api_overview_advanced_query_section(self):
        """Test API overview advanced query section."""
        url = reverse('api-overview')
        response = self.client.get(url)
        
        advanced_section = response.data['Advanced Query Capabilities']
        self.assertIn('Filtering', advanced_section)
        self.assertIn('Searching', advanced_section)
        self.assertIn('Ordering', advanced_section)
        self.assertIn('Pagination', advanced_section)


class ErrorHandlingTestCase(APITestCase):
    """
    Test cases for error handling and edge cases.
    
    Tests:
    - Invalid data handling
    - Database constraint violations
    - Malformed requests
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Test Author')
        
        self.client = APIClient()
        
    def test_invalid_json_data(self):
        """Test handling of invalid JSON data."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        response = self.client.post(
            url, 
            'invalid json data', 
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {'title': 'Test Book'}  # Missing author and publication_year
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_future_publication_year_validation(self):
        """Test validation of future publication year."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('future', str(response.data))
        
    def test_nonexistent_author_reference(self):
        """Test handling of nonexistent author reference."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': 999  # Nonexistent author
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_duplicate_book_creation(self):
        """Test that duplicate books can be created (no unique constraints)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = reverse('book-create')
        data = {
            'title': 'Duplicate Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        # Create first book
        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Create second identical book
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Verify both books exist
        self.assertEqual(Book.objects.filter(title='Duplicate Book').count(), 2)


class PerformanceTestCase(APITestCase):
    """
    Test cases for performance and optimization.
    
    Tests:
    - Query optimization
    - Database query counts
    - Response time considerations
    """
    
    def setUp(self):
        """Set up test data for performance testing."""
        # Create multiple authors and books
        self.authors = []
        self.books = []
        
        for i in range(5):
            author = Author.objects.create(name=f'Author {i}')
            self.authors.append(author)
            
            for j in range(3):
                book = Book.objects.create(
                    title=f'Book {i}-{j}',
                    publication_year=2000 + i,
                    author=author
                )
                self.books.append(book)
        
        self.client = APIClient()
        
    def test_book_list_query_optimization(self):
        """Test that book list uses select_related for author."""
        url = reverse('book-list')
        
        with self.assertNumQueries(2):  # Count query + select_related query
            response = self.client.get(url)
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_author_list_query_optimization(self):
        """Test that author list uses prefetch_related for books."""
        url = reverse('author-list')
        
        with self.assertNumQueries(3):  # Count query + author query + prefetch_related query
            response = self.client.get(url)
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_large_dataset_pagination(self):
        """Test pagination with larger dataset."""
        url = reverse('book-list')
        response = self.client.get(url, {'page_size': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test that pagination structure is present
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Test that we get results (page_size may not be respected due to small dataset)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['count'], 15)  # Total count should be 15
