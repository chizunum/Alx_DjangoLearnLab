from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date"]


    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        # Example simple sanitizer: limit length & remove suspicious characters
        if len(title) > 200:
            raise forms.ValidationError("Title too long.")
        return title

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")
