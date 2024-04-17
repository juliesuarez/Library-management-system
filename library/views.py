from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookAddition, BorrowedBookForm, UserAddition
from .models import Book, BorrowedBook, User

# Create your views here.


def index(request):
    # Render the index page
    return render(request, "index.html")


def user_list(request):
    # Retrieve all users and count them
    users = User.objects.all()
    total_users = users.count()
    # Render the user list page with user data
    return render(
        request, "user_list.html", {"users": users, "total_users": total_users}
    )


def add_user(request):
    # Add a user to the database
    if request.method == "POST":
        form = UserAddition(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to user list page after successful form submission
            return redirect("user_list")
        else:
            # Print form errors for debugging
            print("form is invalid")
            print(form.errors)
    else:
        form = UserAddition()
        print("form is not submitted")
    # Render the add user page
    return render(request, "add_user.html", {"form": form})


def book_list(request):
    # Retrieve all books, count them, calculate total copies, popular books, and genres
    books = Book.objects.all()
    total_books = books.count()
    total_copies = Book.objects.aggregate(total_copies=Sum("copies"))["total_copies"]
    popular_books = Book.get_popular_books()
    popular_genres = Book.get_popular_genres()
    # Render the book list page with book data
    return render(
        request,
        "book_list.html",
        {
            "books": books,
            "total_books": total_books,
            "total_copies": total_copies,
            "popular_books": popular_books,
            "popular_genres": popular_genres,
        },
    )


def add_book(request):
    # Add a book to the database
    if request.method == "POST":
        form = BookAddition(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookAddition()
    # Render the add book page
    return render(request, "add_book.html", {"form": form})


def borrow_book(request):
    # Borrow a book
    if request.method == "POST":
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            # Decrement the count of available copies of the borrowed book
            book = borrowed_book.book
            if book.copies > 0:
                book.copies -= 1
                book.save()
                borrowed_book.save()
            else:
                # Redirect to a page indicating unavailability of the book
                return render(request, "book_unavailable.html", {"book": book})
            # Redirect to borrowed books list after successful borrowing
            return redirect("borrowed_books_list")
    else:
        form = BorrowedBookForm()
    # Render the borrow book page
    return render(request, "borrow_book.html", {"form": form})


def borrowed_books_list(request):
    # Retrieve all borrowed books and count them
    borrowed_books = BorrowedBook.objects.all()
    total_borrowed = BorrowedBook.objects.count()
    # Render the borrowed books list page with borrowed book data
    return render(
        request,
        "borrowed_books_list.html",
        {"borrowed_books": borrowed_books, "total_borrowed": total_borrowed},
    )


@require_POST
def return_book(request, borrowed_book_id):
    # Return a borrowed book
    borrowed_book = get_object_or_404(BorrowedBook, pk=borrowed_book_id)
    # Mark the book as returned
    borrowed_book.returned = True
    borrowed_book.save()
    # Increment the available copies of the book
    borrowed_book.book.copies += 1
    borrowed_book.book.save()
    # Redirect to borrowed books list after successful book return
    return redirect("borrowed_books_list")
