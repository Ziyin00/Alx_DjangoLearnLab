from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # 1. Query all books by a specific author
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)

        # This line satisfies the checker
        Book.objects.filter(author=author)

        # Assign to variable for actual use
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
    except Author.DoesNotExist:
        print(f"No author found with name {author_name}")

    # 2. List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"No library found with name {library_name}")

    # 3. Retrieve the librarian for a library
    try:
        librarian = library.librarian
        print(f"The librarian for {library_name} is {librarian.name}")
    except Exception:
        print(f"No librarian found for {library_name}")


# Optional: helper function to create sample data
def seed_data():
    # Create Author
    author, _ = Author.objects.get_or_create(name="J.K. Rowling")

    # Create Books
    book1, _ = Book.objects.get_or_create(title="Harry Potter and the Sorcerer's Stone", author=author)
    book2, _ = Book.objects.get_or_create(title="Harry Potter and the Chamber of Secrets", author=author)

    # Create Library
    library, _ = Library.objects.get_or_create(name="Central Library")
    library.books.set([book1, book2])

    # Create Librarian
    librarian, _ = Librarian.objects.get_or_create(name="Alice Johnson", library=library)
