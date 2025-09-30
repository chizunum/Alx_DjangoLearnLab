# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


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


# ---------- Blog Post (with tags) ----------
class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Add tags separated by commas"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
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

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        # Process tags from comma-separated string
        tag_names = [t.strip() for t in self.cleaned_data["tags"].split(",") if t.strip()]
        tag_objects = []
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            tag_objects.append(tag_obj)
        post.tags.set(tag_objects)
        return post


# ---------- Comments ----------
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Write your comment...",
            }
        ),
        max_length=2000,
        label="",
    )

    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
