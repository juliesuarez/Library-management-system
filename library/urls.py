from django.urls import path

from .views import (
    add_book,
    add_user,
    book_list,
    borrow_book,
    borrowed_books_list,
    index,
    user_list,
)

urlpatterns = [
    path("", index, name="index"),
    path("add_user/", add_user, name="add_user"),
    path("user_list/", user_list, name="user_list"),
    path("add_book/", add_book, name="add_book"),
    path("book_list/", book_list, name="book_list"),
    path("borrow_book/", borrow_book, name="borrow_book"),
    path("borrowed-books/", borrowed_books_list, name="borrowed-books"),
    path("borrowed_books_list/", borrowed_books_list, name="borrowed_books_list"),
]
