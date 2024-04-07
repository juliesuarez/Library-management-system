from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Count
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r"^\+\d{1,3}\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)  # New field to track available copies
    author = models.CharField(max_length=100)

    @staticmethod
    def get_popular_books():
        return Book.objects.annotate(num_borrowed=Count("borrowedbook")).order_by(
            "-num_borrowed"
        )[:2]

    @staticmethod
    def get_popular_genres():
        return (
            Book.objects.values("genre")
            .annotate(num_books=Count("id"))
            .order_by("-num_books")[:2]
        )

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    borrowed_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new instance
            self.book.copies -= 1  # Decrement the count of available copies
            self.book.save()  # Save the updated book instance
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.book)

    @staticmethod
    def get_overdue_books():
        overdue_books = BorrowedBook.objects.filter(
            due_date__lt=timezone.now(), returned=False
        )
        return overdue_books
