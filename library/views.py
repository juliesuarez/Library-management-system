from django.shortcuts import redirect, render

from .forms import BookAddition, BorrowedBookForm, UserAddition
from .models import Book, BorrowedBook, User


# Create your views here.
def index(request):
    return render(request, "index.html")


def user_list(request):
    users = User.objects.all()
    total_users = users.count()
    return render(
        request, "user_list.html", {"users": users, "total_users": total_users}
    )


def add_user(request):
    if request.method == "POST":
        form = UserAddition(request.POST)
        if form.is_valid():
            print("form is valid")
            # Save the form data to the database
            form.save()
            # Redirect to user list page after successful form submission
            return redirect("user_list")
        else:
            print("form is invalid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserAddition()
        print("form is not submitted")

    return render(request, "add_user.html", {"form": form})


def book_list(request):
    books = Book.objects.all()
    total_books = books.count()
    popular_books = Book.get_popular_books()
    popular_genres = Book.get_popular_genres()
    return render(
        request, "book_list.html", {"books": books, "total_books": total_books, "popular_books": popular_books, "popular_genres": popular_genres}
    )

def add_book(request):
    if request.method == "POST":
        form = BookAddition(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookAddition()

    return render(request, "add_book.html", {"form": form})



def borrow_book(request):
    if request.method == "POST":
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            borrowed_book.save()
            return redirect(
                "borrowed_books_list"
            )  # Redirect to borrowed books list page
    else:
        form = BorrowedBookForm()
    return render(request, "borrow_book.html", {"form": form})


def borrowed_books_list(request):
    borrowed_books = BorrowedBook.objects.all()
    total_borrowed = borrowed_books.count()
    return render(
        request, "borrowed_books_list.html", {"borrowed_books": borrowed_books,'total_borrowed': total_borrowed}
    )
