# Django REST Framework API Project Documentation

## Project Overview

This Django project demonstrates advanced API development using Django REST Framework with custom serializers, nested object handling, and data validation. The project implements a book management system with authors and books, showcasing proper model relationships and serializer patterns.

## Project Structure

```
api_project/
├── api_project/
│   ├── __init__.py
│   ├── settings.py          # Django settings with REST framework configuration
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── api/                     # Main application
│   ├── __init__.py
│   ├── models.py            # Author and Book models with relationships
│   ├── serializers.py       # Custom serializers with validation
│   ├── admin.py             # Django admin configuration
│   ├── views.py             # API views
│   ├── urls.py              # API URL patterns
│   └── migrations/          # Database migrations
├── manage.py                # Django management script
└── db.sqlite3              # SQLite database
```

## Models Implementation

### Author Model

The `Author` model represents book authors with the following characteristics:

```python
class Author(models.Model):
    name = models.CharField(max_length=100, help_text="The full name of the author")
```

**Key Features:**

- Simple model storing author names
- One-to-many relationship with Book model
- Proper string representation for admin interface
- Comprehensive documentation

### Book Model

The `Book` model represents books with detailed information:

```python
class Book(models.Model):
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published", default=2020)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

**Key Features:**

- Foreign key relationship to Author model
- Publication year field with default value
- Cascade deletion (when author is deleted, books are deleted)
- Related name 'books' for reverse relationship access

## Serializers Implementation

### BookSerializer

The `BookSerializer` handles serialization of Book model instances with custom validation:

```python
class BookSerializer(serializers.ModelSerializer):
    def validate_publication_year(self, value):
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

### AuthorSerializer

The `AuthorSerializer` handles author serialization with nested book information:

```python
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
```

**Features:**

- Includes author name field
- Nested BookSerializer for related books
- Dynamic serialization of all books by the author
- Read-only nested books (prevents accidental modifications)

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

2. **Model-Level Validation:**
   - Foreign key constraints ensure data integrity
   - Cascade deletion maintains referential integrity

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
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)
```

**Features:**

- Displays author name and book count
- Search functionality by author name
- Custom method to count related books

### BookAdmin

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')
    list_select_related = ('author',)
```

**Features:**

- Displays book details with author information
- Filtering by author and publication year
- Search by title and author name
- Optimized queries with select_related

## Testing and Verification

### Manual Testing Results

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
- The Great Gatsby (1925) - George Orwell

## Django REST Framework Configuration

### Settings Configuration

The project includes comprehensive REST framework settings:

```python
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

## Usage Instructions

### Running the Project

1. **Start the Development Server:**

   ```bash
   python3 manage.py runserver
   ```

2. **Access Django Admin:**

   - URL: http://127.0.0.1:8000/admin/
   - Username: admin
   - Password: (set during superuser creation)

3. **Create Sample Data:**
   - Add authors through the admin interface
   - Create books with proper author relationships
   - Test the serializers through Django shell

### API Endpoints

The project is configured for API development with:

- REST framework integration
- Custom serializers for data transformation
- Validation and error handling
- Nested object serialization

## Key Implementation Highlights

1. **Proper Model Relationships:**

   - Foreign key relationship between Book and Author
   - Cascade deletion for data integrity
   - Related name for reverse access

2. **Advanced Serialization:**

   - Custom validation with business logic
   - Nested object serialization
   - Read-only fields for data protection

3. **Comprehensive Documentation:**

   - Detailed docstrings for all classes and methods
   - Clear explanation of relationships
   - Usage examples and testing scenarios

4. **Production-Ready Configuration:**
   - Proper admin interface setup
   - REST framework authentication
   - Database optimization with select_related

This implementation demonstrates best practices for Django REST Framework development with custom serializers, nested objects, and data validation, providing a solid foundation for advanced API development.
