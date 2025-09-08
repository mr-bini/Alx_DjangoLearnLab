from relationship_app.models import Author, Library

def books_by_author(author_name):
    return Author.objects.get(name=author_name).books.all()

def books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

def librarian_for_library(library_name):
    return Library.objects.get(name=library_name).librarian
