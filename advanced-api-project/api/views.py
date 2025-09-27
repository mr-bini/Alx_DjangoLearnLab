# views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookUpdateWithoutIDView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # expects JSON: {"id": 1}
        book_id = self.request.data.get("id")
        return Book.objects.get(id=book_id)

class BookDeleteWithoutIDView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get("id")
        return Book.objects.get(id=book_id)
