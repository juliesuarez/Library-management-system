from django import forms

from .models import Book, BorrowedBook, User


class UserAddition(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders
        self.fields["name"].widget.attrs["placeholder"] = "Enter  name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter the email"
        self.fields["phone_number"].widget.attrs[
            "placeholder"
        ] = "Enter the phone number"


class BookAddition(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "genre", "availability", "copies", "author"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders
        self.fields["name"].widget.attrs["placeholder"] = "Enter  name"
        self.fields["genre"].widget.attrs["placeholder"] = "Enter the genre"
        self.fields["availability"].widget.attrs["placeholder"] = "Select"
        self.fields["copies"].widget.attrs["placeholder"] = "Enter the copies"
        self.fields["author"].widget.attrs["placeholder"] = "Enter the author"


class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = [
            "book",
            "due_date",
            "returned",
            "borrowed_date",
            "fine",
            "user_name",
            "number_of_books_borrowed",
        ]
