from .models import Author, Library

# Query all books by a specific author
def books_by_author(author_name):
    return Author.objects.get(name=author_name).books.all()

# List all books in a library
def books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    return Library.objects.get(name=library_name).librarian
