from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),                     # List
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),        # Detail
    path('books/create/', BookCreateView.as_view(), name='book-create'),          # Create
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # Update
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # Delete
    path('books/update', BookUpdateWithoutIDView.as_view(), name='book-update'),
path('books/delete', BookDeleteWithoutIDView.as_view(), name='book-delete'),

]
