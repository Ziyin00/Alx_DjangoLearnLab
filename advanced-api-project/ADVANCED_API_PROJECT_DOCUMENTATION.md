# Advanced API Project - Django REST Framework Implementation

## Project Overview

This is a comprehensive Django REST Framework project demonstrating advanced API development with custom serializers, nested object handling, and data validation. The project implements a sophisticated book management system with authors and books, showcasing proper model relationships and serializer patterns.

## Project Structure

```
advanced-api-project/
├── advanced_api_project/          # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Django settings with REST framework configuration
│   ├── urls.py                   # Main URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
├── api/                          # Main application
│   ├── __init__.py
│   ├── models.py                 # Author and Book models with relationships
│   ├── serializers.py            # Custom serializers with validation
│   ├── admin.py                  # Django admin configuration
│   ├── views.py                  # API views
│   ├── urls.py                   # API URL patterns
│   ├── tests.py                  # Test cases
│   └── migrations/               # Database migrations
├── manage.py                     # Django management script
├── db.sqlite3                   # SQLite database
└── ADVANCED_API_PROJECT_DOCUMENTATION.md
```

## Models Implementation

### Author Model

The `Author` model represents book authors with comprehensive documentation:

```python
class Author(models.Model):
    """
    Author model representing a book author.

    This model stores basic information about authors who write books.
    It has a one-to-many relationship with the Book model, meaning
    one author can have multiple books.
    """
    name = models.CharField(max_length=100, help_text="The full name of the author")
```

**Key Features:**

- Simple model storing author names
- One-to-many relationship with Book model
- Proper string representation for admin interface
- Comprehensive documentation with docstrings
- Help text for form fields

### Book Model

The `Book` model represents books with detailed information and relationships:

```python
class Book(models.Model):
    """
    Book model representing a book with its details.

    This model stores information about books including title, publication year,
    and a foreign key relationship to the Author model. The relationship
    establishes that each book has one author, but an author can have multiple books.
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published", default=2020)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )
```

**Key Features:**

- Foreign key relationship to Author model
- Publication year field with default value
- Cascade deletion (when author is deleted, books are deleted)
- Related name 'books' for reverse relationship access
- Comprehensive field documentation

## Serializers Implementation

### BookSerializer

The `BookSerializer` handles serialization of Book model instances with custom validation:

```python
class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of Book model instances.

    This serializer includes all fields of the Book model and implements
    custom validation to ensure the publication_year is not in the future.
    The author field is serialized as a foreign key relationship.
    """

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.

        Args:
            value (int): The publication year to validate

        Returns:
            int: The validated publication year

        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
```

**Features:**

- Serializes all Book model fields
- Custom validation for publication year (prevents future years)
- Proper error handling with descriptive messages
- Read-only ID field
- Comprehensive documentation

### AuthorSerializer

The `AuthorSerializer` handles author serialization with nested book information:

```python
class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of Author model instances.

    This serializer includes the author's name field and dynamically serializes
    related books using the BookSerializer. The relationship between Author
    and Book is handled through the 'books' related_name, allowing for nested
    serialization of all books written by the author.
    """
    books = BookSerializer(many=True, read_only=True)
```

**Features:**

- Includes author name field
- Nested BookSerializer for related books
- Dynamic serialization of all books by the author
- Read-only nested books (prevents accidental modifications)
- Comprehensive documentation

## Database Relationships

### One-to-Many Relationship

The relationship between Author and Book models follows a one-to-many pattern:

- **One Author** can have **Many Books**
- **One Book** belongs to **One Author**
- Implemented using `ForeignKey` field in Book model
- Related name 'books' allows reverse access: `author.books.all()`

### Relationship Handling in Serializers

1. **Forward Relationship (Book → Author):**

   - BookSerializer includes author field as foreign key ID
   - Author information accessible through `book.author.name`

2. **Reverse Relationship (Author → Books):**
   - AuthorSerializer includes nested books using BookSerializer
   - All books by an author are serialized automatically
   - Nested serialization is read-only for data integrity

## Validation Implementation

### Custom Validation Rules

1. **Publication Year Validation:**

   - Prevents books from having future publication years
   - Uses current year comparison
   - Provides clear error messages
   - Validates at serializer level

2. **Model-Level Validation:**
   - Foreign key constraints ensure data integrity
   - Cascade deletion maintains referential integrity
   - Default values for required fields

### Validation Testing

The validation system was tested with:

- Valid book creation with past publication years
- Invalid book creation with future publication years
- Proper error message generation
- Nested object validation

## Django Admin Configuration

### AuthorAdmin

```python
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.

    Provides a user-friendly interface for managing authors in the Django admin.
    Includes list display, filtering, and search capabilities.
    """
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)

    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'
```

**Features:**

- Displays author name and book count
- Search functionality by author name
- Custom method to count related books
- Comprehensive documentation

### BookAdmin

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    Provides a user-friendly interface for managing books in the Django admin.
    Includes list display, filtering, and search capabilities with proper
    foreign key relationship handling.
    """
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')
    ordering = ('title',)
    list_select_related = ('author',)
```

**Features:**

- Displays book details with author information
- Filtering by author and publication year
- Search by title and author name
- Optimized queries with select_related
- Comprehensive documentation

## Django REST Framework Configuration

### Settings Configuration

The project includes comprehensive REST framework settings:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**Features:**

- Token and session authentication
- Authenticated access required
- Pagination with 10 items per page
- REST framework properly installed and configured
- API app included in installed apps

## Testing and Verification

### Comprehensive Testing Results

The implementation was tested with the following scenarios:

1. **Model Creation:**

   - ✅ Author creation with name field
   - ✅ Book creation with title, publication year, and author
   - ✅ Foreign key relationship establishment

2. **Serializer Functionality:**

   - ✅ Book serialization with all fields
   - ✅ Author serialization with nested books
   - ✅ Custom validation for publication year
   - ✅ Error handling for invalid data

3. **Validation Testing:**

   - ✅ Future publication year rejection
   - ✅ Valid book creation acceptance
   - ✅ Proper error message generation

4. **Relationship Testing:**
   - ✅ Author-Book relationship verification
   - ✅ Nested serialization functionality
   - ✅ Reverse relationship access

### Test Data Created

During testing, the following sample data was created:

**Authors:**

- J.K. Rowling
- George Orwell
- F. Scott Fitzgerald

**Books:**

- Harry Potter and the Philosopher's Stone (1997) - J.K. Rowling
- Harry Potter and the Chamber of Secrets (1998) - J.K. Rowling
- 1984 (1949) - George Orwell
- Animal Farm (1945) - George Orwell
- The Great Gatsby (1925) - F. Scott Fitzgerald

## Usage Instructions

### Running the Advanced API Project

1. **Navigate to the Project Directory:**

   ```bash
   cd /Users/macbook/Desktop/pro/2025/alx/Alx_DjangoLearnLab/advanced-api-project
   ```

2. **Start the Development Server:**

   ```bash
   python3 manage.py runserver
   ```

3. **Access Django Admin:**

   - URL: http://127.0.0.1:8000/admin/
   - Username: admin
   - Password: (set during superuser creation)

4. **Create Sample Data:**
   - Add authors through the admin interface
   - Create books with proper author relationships
   - Test the serializers through Django shell

### API Development Ready

The project is configured for advanced API development with:

- REST framework integration
- Custom serializers for data transformation
- Validation and error handling
- Nested object serialization
- Authentication and permissions
- Pagination support

## Key Implementation Highlights

1. **Advanced Model Relationships:**

   - Foreign key relationship between Book and Author
   - Cascade deletion for data integrity
   - Related name for reverse access
   - Comprehensive field documentation

2. **Sophisticated Serialization:**

   - Custom validation with business logic
   - Nested object serialization
   - Read-only fields for data protection
   - Comprehensive error handling

3. **Production-Ready Configuration:**

   - Proper admin interface setup
   - REST framework authentication
   - Database optimization with select_related
   - Comprehensive documentation

4. **Advanced Features:**
   - Custom validation rules
   - Nested serialization
   - Relationship handling
   - Error message customization

## Project Benefits

This advanced API project demonstrates:

- **Best Practices**: Proper Django and DRF patterns
- **Scalability**: Well-structured for growth
- **Maintainability**: Comprehensive documentation
- **Security**: Authentication and permissions
- **Performance**: Optimized queries and pagination
- **User Experience**: Intuitive admin interface

## Next Steps for Development

1. **API Views**: Implement ViewSets and API views
2. **URL Routing**: Configure API endpoints
3. **Authentication**: Implement token-based authentication
4. **Testing**: Add comprehensive test suite
5. **Documentation**: API documentation with Swagger
6. **Deployment**: Production deployment configuration

This implementation provides a solid foundation for advanced Django REST Framework development with custom serializers, nested objects, and data validation, demonstrating professional-level API development practices.
