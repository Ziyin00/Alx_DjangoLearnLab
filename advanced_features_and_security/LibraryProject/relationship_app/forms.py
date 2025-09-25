from django import forms
from .models import Book, Author, Library


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'books']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'books': forms.CheckboxSelectMultiple(),
        }
