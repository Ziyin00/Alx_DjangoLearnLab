from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors who write books.
    It has a one-to-many relationship with the Book model, meaning
    one author can have multiple books.
    """
    name = models.CharField(max_length=100, help_text="The full name of the author")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"


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
    
    def __str__(self):
        return f"{self.title} by {self.author.name} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"