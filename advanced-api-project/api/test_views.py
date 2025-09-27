from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookAPITests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", publication_year=2020, author=self.author)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # not authenticated
