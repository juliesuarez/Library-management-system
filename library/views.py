from django.shortcuts import redirect, render

from .forms import BookAddition, BorrowedBookForm, UserAddition
from .models import Book, BorrowedBook, User
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
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
    total_copies = Book.objects.aggregate(total_copies=Sum('copies'))['total_copies']
    popular_books = Book.get_popular_books()
    popular_genres = Book.get_popular_genres()
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
            
            # Decrement the count of available copies of the borrowed book
            book = borrowed_book.book
            if book.copies > 0:
                book.copies -= 1
                book.save()
                borrowed_book.save()
            else:
                # Redirect to a page indicating unavailability of the book
                return render(request, "book_unavailable.html", {"book": book})
                
            return redirect("borrowed_books_list")
    else:
        form = BorrowedBookForm()
    return render(request, "borrow_book.html", {"form": form})


def borrowed_books_list(request):
    borrowed_books = BorrowedBook.objects.all()
    total_borrowed = BorrowedBook.objects.count()  
    return render(
        request,
        "borrowed_books_list.html",
        {"borrowed_books": borrowed_books, "total_borrowed": total_borrowed},
    )

@require_POST
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, pk=borrowed_book_id)
    
    # Mark the book as returned
    borrowed_book.returned = True
    borrowed_book.save()

    # Increment the available copies of the book
    borrowed_book.book.copies += 1
    borrowed_book.book.save()

    return redirect('borrowed_books_list')  # Redirect to a view showing borrowed books
