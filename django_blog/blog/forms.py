# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post


# ---------- User Registration ----------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


# ---------- User Profile ----------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")


# ---------- Blog Post ----------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full border rounded p-2",
                    "placeholder": "Post title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full border rounded p-2",
                    "rows": 8,
                    "placeholder": "Write your post...",
                }
            ),
        }
