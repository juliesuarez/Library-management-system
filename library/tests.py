# Create your tests here.
from django.test import TestCase
from django.utils import timezone

from .models import Book, BorrowedBook, User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="John Doe", email="john@example.com", phone_number="+1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(name="Book1", genre="Fiction", author="Author1")

    def test_book_creation(self):
        self.assertEqual(Book.objects.count(), 1)


class BorrowedBookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(name="Book1", genre="Fiction", author="Author1")
        self.user = User.objects.create(
            name="John Doe", email="john@example.com", phone_number="+1234567890"
        )
        self.borrowed_book = BorrowedBook.objects.create(
            book=self.book, user_name=self.user.name, due_date=timezone.now()
        )

    def test_get_overdue_books(self):
        overdue_books = BorrowedBook.get_overdue_books()
        self.assertEqual(overdue_books.count(), 1)


class BookMethodTests(TestCase):
    def test_get_popular_books(self):
        book1 = Book.objects.create(name="Book1", genre="Fiction", author="Author1")
        book2 = Book.objects.create(name="Book2", genre="Fiction", author="Author2")
        BorrowedBook.objects.create(
            book=book1, user_name="User1", due_date=timezone.now()
        )
        BorrowedBook.objects.create(
            book=book2, user_name="User2", due_date=timezone.now()
        )
        popular_books = Book.get_popular_books()
        self.assertEqual(popular_books.count(), 2)

    def test_get_popular_genres(self):
        book1 = Book.objects.create(name="Book1", genre="Fiction", author="Author1")
        book2 = Book.objects.create(name="Book2", genre="Fiction", author="Author2")
        popular_genres = Book.get_popular_genres()
        self.assertEqual(popular_genres.count(), 1)
