from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Book, Library

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# Role checks
def is_admin(user): return hasattr(user, "userprofile") and user.userprofile.role == "Admin"
def is_librarian(user): return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"
def is_member(user): return hasattr(user, "userprofile") and user.userprofile.role == "Member"

@user_passes_test(is_admin)
def admin_view(request): return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request): return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request): return render(request, "relationship_app/member_view.html")

# Permissions-based views
@permission_required("relationship_app.can_add_book")
def add_book(request): return render(request, "relationship_app/add_book.html")

@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id): return render(request, "relationship_app/edit_book.html")

@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id): return redirect("list_books")
