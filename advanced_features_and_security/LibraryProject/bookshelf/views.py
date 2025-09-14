from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.add_book', raise_exception=True)
def add_book(request):
    return render(request, 'bookshelf/form_example.html')

@permission_required('bookshelf.change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookshelf/form_example.html', {'book': book})

@permission_required('bookshelf.delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookshelf/confirm_delete.html', {'book': book})
